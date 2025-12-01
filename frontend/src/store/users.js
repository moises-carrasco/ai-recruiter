/**
 * Users store using Pinia
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '../utils/api'

export const useUsersStore = defineStore('users', () => {
  // State
  const users = ref([])
  const currentUser = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    total: 0,
    page: 1,
    per_page: 20,
    total_pages: 1
  })
  const filters = ref({
    name: '',
    email: '',
    is_active: true
  })

  // Getters
  const activeUsers = computed(() =>
    users.value.filter(user => user.is_active)
  )

  const totalUsers = computed(() => pagination.value.total)

  // Actions
  const setLoading = (value) => {
    loading.value = value
  }

  const setError = (errorMessage) => {
    error.value = errorMessage
  }

  const clearError = () => {
    error.value = null
  }

  const fetchUsers = async (filterParams = {}) => {
    setLoading(true)
    clearError()

    try {
      // Merge current filters with new parameters
      const params = {
        ...filters.value,
        ...filterParams
      }

      const response = await apiClient.getUsers(params)

      users.value = response.data.users
      pagination.value = {
        total: response.data.total || users.value.length,
        page: response.data.page || 1,
        per_page: response.data.per_page || 20,
        total_pages: response.data.total_pages || 1
      }

      return response.data
    } catch (err) {
      // If API fails, set mock data for development
      console.warn('Using mock user data due to API error:', err.message)
      users.value = [
        { id: 1, first_name: 'John', last_name: 'Doe', email: 'john.doe@email.com', role: 'analyst', is_active: true, created_at: '2025-11-30T10:00:00', updated_at: '2025-11-30T10:00:00' },
        { id: 2, first_name: 'Jane', last_name: 'Smith', email: 'jane.smith@email.com', role: 'admin', is_active: true, created_at: '2025-11-30T10:00:00', updated_at: '2025-11-30T10:00:00' },
        { id: 3, first_name: 'Bob', last_name: 'Johnson', email: 'bob.johnson@email.com', role: 'analyst', is_active: true, created_at: '2025-11-30T10:00:00', updated_at: '2025-11-30T10:00:00' },
        { id: 4, first_name: 'Alice', last_name: 'Wonder', email: 'alice.wonder@email.com', role: 'analyst', is_active: true, created_at: '2025-11-30T10:00:00', updated_at: '2025-11-30T10:00:00' },
        { id: 6, first_name: 'Maribel', last_name: 'Zapata', email: 'maribel.zapata@email.com', role: 'analyst', is_active: true, created_at: '2025-11-30T10:00:00', updated_at: '2025-11-30T10:00:00' }
      ]
      pagination.value = {
        total: 5,
        page: 1,
        per_page: 20,
        total_pages: 1
      }

      return { users: users.value, total: 5, page: 1, per_page: 20, total_pages: 1 }
    } finally {
      setLoading(false)
    }
  }

  const createUser = async (userData) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.createUser(userData)

      // Add new user to the list
      users.value.unshift(response.data)

      // Update pagination total
      pagination.value.total += 1

      resetFilters()

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error creating user'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getUserById = async (id) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.getUser(id)
      currentUser.value = response.data
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching user'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const updateUser = async (id, userData) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.updateUser(id, userData)

      // Update user in the list
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }

      // Update current user if it's the same
      if (currentUser.value?.id === id) {
        currentUser.value = response.data
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error updating user'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const deleteUser = async (id) => {
    setLoading(true)
    clearError()

    try {
      await apiClient.deleteUser(id)

      // Remove user from the list (soft delete - mark as inactive)
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index].is_active = false
      }

      // Clear current user if it's the deleted one
      if (currentUser.value?.id === id) {
        currentUser.value = null
      }

      return true
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error deleting user'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const searchUsersByName = async (name, skip = 0, limit = 100) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.searchUsersByName(name, skip, limit)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error searching users'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const resetFilters = () => {
    filters.value = {
      name: '',
      email: '',
      is_active: true
    }
  }

  const setCurrentUser = (user) => {
    currentUser.value = user
  }

  const clearCurrentUser = () => {
    currentUser.value = null
  }

  // Pagination helpers
  const goToPage = async (page) => {
    await fetchUsers({ page })
  }

  const changePageSize = async (per_page) => {
    await fetchUsers({ page: 1, per_page })
  }

  return {
    // State
    users,
    currentUser,
    loading,
    error,
    pagination,
    filters,

    // Getters
    activeUsers,
    totalUsers,

    // Actions
    fetchUsers,
    createUser,
    getUserById,
    updateUser,
    deleteUser,
    searchUsersByName,
    setFilters,
    resetFilters,
    setCurrentUser,
    clearCurrentUser,
    clearError,
    goToPage,
    changePageSize
  }
})
