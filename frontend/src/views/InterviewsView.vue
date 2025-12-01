<template>
  <div class="interviews-view">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Interviews</h1>
          <p class="mt-2 text-sm text-gray-600">
            Manage and schedule candidate interviews
          </p>
        </div>
        <button
          @click="showCreateForm"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Interview
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white p-4 rounded-lg shadow mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Role Filter -->
        <div>
          <label for="roleFilter" class="block text-sm font-medium text-gray-700 mb-1">
            Filter by Role
          </label>
          <select
            id="roleFilter"
            v-model="filters.role_id"
            @change="applyFilters"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Roles</option>
            <option
              v-for="role in roles"
              :key="role.id"
              :value="role.id"
            >
              {{ role.text_value }}
            </option>
          </select>
        </div>

        <!-- Client Filter -->
        <div>
          <label for="clientFilter" class="block text-sm font-medium text-gray-700 mb-1">
            Filter by Client
          </label>
          <select
            id="clientFilter"
            v-model="filters.client_id"
            @change="applyFilters"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Clients</option>
            <option
              v-for="client in clients"
              :key="client.id"
              :value="client.id"
            >
              {{ client.text_value }}
            </option>
          </select>
        </div>

        <!-- Status Filter -->
        <div>
          <label for="statusFilter" class="block text-sm font-medium text-gray-700 mb-1">
            Filter by Status
          </label>
          <select
            id="statusFilter"
            v-model="filters.status_id"
            @change="applyFilters"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Statuses</option>
            <option
              v-for="status in interviewStatuses"
              :key="status.id"
              :value="status.id"
            >
              {{ status.text_value }}
            </option>
          </select>
        </div>
      </div>

      <!-- Clear Filters -->
      <div class="mt-4 flex justify-end">
        <button
          @click="clearFilters"
          class="text-sm text-gray-600 hover:text-gray-900 underline"
        >
          Clear filters
        </button>
      </div>
    </div>

    <!-- Interview List -->
    <InterviewList
      :interviews="interviewsStore.interviews"
      :loading="interviewsStore.loading"
      :pagination="interviewsStore.pagination"
      @view="handleViewInterview"
      @edit="handleEditInterview"
      @delete="handleDeleteInterview"
      @copy-link="handleCopyInterviewLink"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-4 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white max-h-screen overflow-y-auto">
        <div class="mt-3">
          <InterviewForm
            :interview="editingInterview"
            :loading="formLoading"
            @save="handleSaveInterview"
            @cancel="hideForm"
          />
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message.text" class="fixed bottom-4 right-4 z-50">
      <div
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium',
          message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]"
      >
        {{ message.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import InterviewList from '../components/lists/InterviewList.vue'
import InterviewForm from '../components/forms/InterviewForm.vue'
import { useInterviewsStore } from '../store/interviews'
import { useLookupStore } from '../store/lookup'

// Router
const router = useRouter()

// Stores
const interviewsStore = useInterviewsStore()
const lookupStore = useLookupStore()

// State
const showForm = ref(false)
const editingInterview = ref(null)
const formLoading = ref(false)
const message = ref({ text: '', type: '' })
const filters = ref({
  role_id: '',
  client_id: '',
  status_id: ''
})

// Computed
const roles = computed(() => lookupStore.roles || [])
const clients = computed(() => lookupStore.clients || [])
const interviewStatuses = computed(() => lookupStore.interviewStatuses || [])

// Methods
const loadInterviews = async () => {
  try {
    await interviewsStore.fetchInterviews()
  } catch (error) {
    showMessage('Error loading interviews', 'error')
  }
}

const loadLookupData = async () => {
  try {
    if (!lookupStore.roles.length) {
      await lookupStore.fetchLookupData()
    }
  } catch (error) {
    showMessage('Error loading lookup data', 'error')
  }
}

const showCreateForm = () => {
  editingInterview.value = null
  showForm.value = true
}

const handleViewInterview = (interview) => {
  router.push(`/interviews/${interview.id}`)
}

const handleEditInterview = (interview) => {
  editingInterview.value = interview
  showForm.value = true
}

const handleDeleteInterview = async (interviewId) => {
  if (confirm('Are you sure you want to delete this interview?')) {
    try {
      await interviewsStore.deleteInterview(interviewId)
      showMessage('Interview deleted successfully', 'success')
    } catch (error) {
      showMessage('Error deleting interview', 'error')
    }
  }
}

const handleCopyInterviewLink = (interview) => {
  try {
    const link = interviewsStore.copyInterviewLink(interview)
    if (link) {
      navigator.clipboard.writeText(link)
      showMessage('Interview link copied to clipboard', 'success')
    }
  } catch (error) {
    showMessage('Error copying interview link', 'error')
  }
}

const handleSaveInterview = async (interviewData) => {
  formLoading.value = true
  try {
    if (editingInterview.value) {
      await interviewsStore.updateInterview(editingInterview.value.id, interviewData)
      showMessage('Interview updated successfully', 'success')
    } else {
      await interviewsStore.createInterview(interviewData)
      showMessage('Interview created successfully', 'success')
    }
    hideForm()
  } catch (error) {
    showMessage('Error saving interview', 'error')
  } finally {
    formLoading.value = false
  }
}

const hideForm = () => {
  showForm.value = false
  editingInterview.value = null
  formLoading.value = false
}

const applyFilters = async () => {
  const filterParams = { ...filters.value, page: 1 }
  try {
    await interviewsStore.fetchInterviews(filterParams)
  } catch (error) {
    showMessage('Error applying filters', 'error')
  }
}

const clearFilters = async () => {
  filters.value = {
    role_id: '',
    client_id: '',
    status_id: ''
  }
  try {
    await interviewsStore.fetchInterviews({ page: 1 })
  } catch (error) {
    showMessage('Error clearing filters', 'error')
  }
}

const handlePageChange = async (page) => {
  try {
    await interviewsStore.goToPage(page)
  } catch (error) {
    showMessage('Error changing page', 'error')
  }
}

const showMessage = (text, type) => {
  message.value = { text, type }
  setTimeout(() => {
    message.value = { text: '', type: '' }
  }, 3000)
}

// Lifecycle
onMounted(async () => {
  await loadLookupData()
  await loadInterviews()
})
</script>
