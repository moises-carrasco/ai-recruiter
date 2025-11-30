<template>
  <div class="users-view">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">Users</h2>
          <p class="mt-1 text-sm text-gray-600">
            Manage system users and their access permissions
          </p>
        </div>
        <button
          @click="showCreateForm = true"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add User
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="usersStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-600">{{ usersStore.error }}</p>
        </div>
        <div class="ml-auto pl-3">
          <button
            @click="usersStore.clearError()"
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
      :filters="usersStore.filters"
      :total-results="usersStore.pagination.total"
      :loading="usersStore.loading"
      @filter-change="handleFilterChange"
      @page-size-change="handlePageSizeChange"
      @clear-filters="handleClearFilters"
    />

    <!-- Users List -->
    <UserList
      :users="usersStore.users"
      :loading="usersStore.loading"
      :pagination="usersStore.pagination"
      @edit="handleEditUser"
      @delete="handleDeleteUser"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Modal -->
    <div v-if="showCreateForm || showEditForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border max-w-2xl shadow-lg rounded-md bg-white">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ showEditForm ? 'Edit User' : 'Add New User' }}
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

        <UserForm
          :user="selectedUser"
          :loading="usersStore.loading"
          @save="handleSaveUser"
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
import { useUsersStore } from '../store/users'
import UserList from '../components/lists/UserList.vue'
import UserForm from '../components/forms/UserForm.vue'
import FilterControls from '../components/lists/FilterControls.vue'

// Store
const usersStore = useUsersStore()

// State
const showCreateForm = ref(false)
const showEditForm = ref(false)
const selectedUser = ref(null)
const successMessage = ref('')

// Methods
const loadUsers = async (filters = {}) => {
  try {
    await usersStore.fetchUsers(filters)
  } catch (error) {
    console.error('Error loading users:', error)
  }
}

const handleFilterChange = async (filters) => {
  usersStore.setFilters(filters)
  await loadUsers(filters)
}

const handlePageSizeChange = async (filters) => {
  usersStore.setFilters(filters)
  await loadUsers(filters)
}

const handleClearFilters = async (filters) => {
  usersStore.resetFilters()
  await loadUsers(filters)
}

const handlePageChange = async (page) => {
  const filters = { ...usersStore.filters, page }
  usersStore.setFilters(filters)
  await loadUsers(filters)
}

const handleEditUser = (user) => {
  selectedUser.value = user
  showEditForm.value = true
}

const handleDeleteUser = async (userId) => {
  try {
    await usersStore.deleteUser(userId)
    successMessage.value = 'User deleted successfully'

    // Auto-hide success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    // Reload users to reflect changes
    await loadUsers(usersStore.filters)
  } catch (error) {
    console.error('Error deleting user:', error)
  }
}

const handleSaveUser = async (userData) => {
  try {
    if (showEditForm.value && selectedUser.value) {
      await usersStore.updateUser(selectedUser.value.id, userData)
      successMessage.value = 'User updated successfully'
    } else {
      await usersStore.createUser(userData)
      successMessage.value = 'User created successfully'
    }

    closeModal()

    // Auto-hide success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    // Reload users to reflect changes
    await loadUsers(usersStore.filters)
  } catch (error) {
    console.error('Error saving user:', error)
  }
}

const closeModal = () => {
  showCreateForm.value = false
  showEditForm.value = false
  selectedUser.value = null
}

// Lifecycle
onMounted(async () => {
  await loadUsers()
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
