/**
 * Candidates store using Pinia
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '../utils/api'

export const useCandidatesStore = defineStore('candidates', () => {
  // State
  const candidates = ref([])
  const currentCandidate = ref(null)
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
  const activeCandidates = computed(() => 
    candidates.value.filter(candidate => candidate.is_active)
  )

  const totalCandidates = computed(() => pagination.value.total)

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

  const fetchCandidates = async (filterParams = {}) => {
    setLoading(true)
    clearError()
    
    try {
      // Merge current filters with new parameters
      const params = {
        ...filters.value,
        ...filterParams
      }

      const response = await apiClient.getCandidates(params)
      
      candidates.value = response.data.candidates
      pagination.value = {
        total: response.data.total,
        page: response.data.page,
        per_page: response.data.per_page,
        total_pages: response.data.total_pages
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching candidates'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const createCandidate = async (candidateData) => {
    setLoading(true)
    clearError()
    
    try {
      const response = await apiClient.createCandidate(candidateData)
      
      // Add new candidate to the list
      candidates.value.unshift(response.data)
      
      // Update pagination total
      pagination.value.total += 1

      resetFilters()
      
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error creating candidate'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getCandidateById = async (id) => {
    setLoading(true)
    clearError()
    
    try {
      const response = await apiClient.getCandidate(id)
      currentCandidate.value = response.data
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching candidate'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const updateCandidate = async (id, candidateData) => {
    setLoading(true)
    clearError()
    
    try {
      const response = await apiClient.updateCandidate(id, candidateData)
      
      // Update candidate in the list
      const index = candidates.value.findIndex(candidate => candidate.id === id)
      if (index !== -1) {
        candidates.value[index] = response.data
      }
      
      // Update current candidate if it's the same
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = response.data
      }
      
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error updating candidate'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const deleteCandidate = async (id) => {
    setLoading(true)
    clearError()
    
    try {
      await apiClient.deleteCandidate(id)
      
      // Remove candidate from the list (soft delete - mark as inactive)
      const index = candidates.value.findIndex(candidate => candidate.id === id)
      if (index !== -1) {
        candidates.value[index].is_active = false
      }
      
      // Clear current candidate if it's the deleted one
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = null
      }
      
      return true
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error deleting candidate'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const searchCandidatesByName = async (name, skip = 0, limit = 100) => {
    setLoading(true)
    clearError()
    
    try {
      const response = await apiClient.searchCandidatesByName(name, skip, limit)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error searching candidates'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getCandidateByEmail = async (email) => {
    setLoading(true)
    clearError()
    
    try {
      const response = await apiClient.getCandidateByEmail(email)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching candidate by email'
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

  const setCurrentCandidate = (candidate) => {
    currentCandidate.value = candidate
  }

  const clearCurrentCandidate = () => {
    currentCandidate.value = null
  }

  // Pagination helpers
  const goToPage = async (page) => {
    await fetchCandidates({ page })
  }

  const changePageSize = async (per_page) => {
    await fetchCandidates({ page: 1, per_page })
  }

  return {
    // State
    candidates,
    currentCandidate,
    loading,
    error,
    pagination,
    filters,
    
    // Getters
    activeCandidates,
    totalCandidates,
    
    // Actions
    fetchCandidates,
    createCandidate,
    getCandidateById,
    updateCandidate,
    deleteCandidate,
    searchCandidatesByName,
    getCandidateByEmail,
    setFilters,
    resetFilters,
    setCurrentCandidate,
    clearCurrentCandidate,
    clearError,
    goToPage,
    changePageSize
  }
})
