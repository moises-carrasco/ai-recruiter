<template>
  <div class="candidates-view">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Candidates</h2>
          <p class="mt-1 text-sm text-gray-600">
            Manage candidate information and track their interview progress
          </p>
        </div>
        <button
          @click="openCreateForm"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add Candidate
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="candidatesStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-600">{{ candidatesStore.error }}</p>
        </div>
        <div class="ml-auto pl-3">
          <button
            @click="candidatesStore.clearError()"
            class="inline-flex text-red-400 hover:text-red-600"
          >
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Filter Controls -->
    <FilterControls
      :filters="candidatesStore.filters"
      :total-results="candidatesStore.pagination.total"
      :loading="candidatesStore.loading"
      @filter-change="handleFilterChange"
      @page-size-change="handlePageSizeChange"
      @clear-filters="handleClearFilters"
    />

    <!-- Candidates List -->
    <CandidateList
      :candidates="candidatesStore.candidates"
      :loading="candidatesStore.loading"
      :pagination="candidatesStore.pagination"
      @edit="handleEditCandidate"
      @delete="handleDeleteCandidate"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Modal -->
    <div v-if="showCreateForm || showEditForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border max-w-2xl shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ showEditForm ? 'Edit Candidate' : 'Add New Candidate' }}
          </h3>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <CandidateForm
          :candidate="selectedCandidate"
          :loading="candidatesStore.loading"
          @save="handleSaveCandidate"
          @cancel="closeModal"
        />
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="fixed bottom-4 right-4 z-50">
      <div class="bg-green-50 border border-green-200 rounded-md p-4 shadow-lg">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-green-600">{{ successMessage }}</p>
          </div>
          <div class="ml-auto pl-3">
            <button
              @click="successMessage = ''"
              class="inline-flex text-green-400 hover:text-green-600"
            >
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCandidatesStore } from '../store/candidates'
import CandidateList from '../components/lists/CandidateList.vue'
import CandidateForm from '../components/forms/CandidateForm.vue'
import FilterControls from '../components/lists/FilterControls.vue'

// Store
const candidatesStore = useCandidatesStore()

// State
const showCreateForm = ref(false)
const showEditForm = ref(false)
const selectedCandidate = ref(null)
const successMessage = ref('')

// Methods
const loadCandidates = async (filters = {}) => {
  try {
    await candidatesStore.fetchCandidates(filters)
  } catch (error) {
    console.error('Error loading candidates:', error)
  }
}

const handleFilterChange = async (filters) => {
  candidatesStore.setFilters(filters)
  await loadCandidates(filters)
}

const handlePageSizeChange = async (filters) => {
  candidatesStore.setFilters(filters)
  await loadCandidates(filters)
}

const handleClearFilters = async (filters) => {
  candidatesStore.resetFilters()
  await loadCandidates(filters)
}

const handlePageChange = async (page) => {
  const filters = { ...candidatesStore.filters, page }
  candidatesStore.setFilters(filters)
  await loadCandidates(filters)
}

const openCreateForm = () => {
  // Clear any previous errors and reset form state
  candidatesStore.clearError()
  selectedCandidate.value = null // Ensure we're in create mode
  showCreateForm.value = true
}

const handleEditCandidate = (candidate) => {
  selectedCandidate.value = candidate
  showEditForm.value = true
}

const handleDeleteCandidate = async (candidateId) => {
  try {
    await candidatesStore.deleteCandidate(candidateId)
    successMessage.value = 'Candidate deleted successfully'

    // Auto-hide success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    // Note: No need to reload candidates - store already marked candidate as inactive
  } catch (error) {
    console.error('Error deleting candidate:', error)
  }
}

const handleSaveCandidate = async (candidateData) => {
  try {
    if (showEditForm.value && selectedCandidate.value) {
      await candidatesStore.updateCandidate(selectedCandidate.value.id, candidateData)
      successMessage.value = 'Candidate updated successfully'
    } else {
      await candidatesStore.createCandidate(candidateData)
      successMessage.value = 'Candidate created successfully'

      // Clear any potential lingering errors after successful creation
      candidatesStore.clearError()
    }

    closeModal()

    // Auto-hide success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    // Note: No need to reload candidates - store already updated the local list
  } catch (error) {
    console.error('Error saving candidate:', error)
  }
}

const closeModal = () => {
  showCreateForm.value = false
  showEditForm.value = false
  selectedCandidate.value = null
}

// Lifecycle
onMounted(async () => {
  await loadCandidates()
})

// Auto-clear success message
watch(successMessage, (newMessage) => {
  if (newMessage) {
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
  }
})
</script>
