/**
 * Interviews store using Pinia
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '../utils/api'

export const useInterviewsStore = defineStore('interviews', () => {
  // State
  const interviews = ref([])
  const currentInterview = ref(null)
  const interviewWithFeedback = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    total: 0,
    page: 1,
    per_page: 20,
    total_pages: 1
  })
  const filters = ref({
    analyst_id: null,
    candidate_id: null,
    role_id: null,
    client_id: null,
    status_id: null,
    scheduled_from: null,
    scheduled_to: null
  })

  // Getters
  const activeInterviews = computed(() =>
    interviews.value.filter(interview => interview.status_text !== 'Cancelled')
  )

  const totalInterviews = computed(() => pagination.value.total)

  const interviewsByStatus = computed(() => {
    const grouped = {}
    interviews.value.forEach(interview => {
      const status = interview.status_text || 'Unknown'
      if (!grouped[status]) {
        grouped[status] = []
      }
      grouped[status].push(interview)
    })
    return grouped
  })

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

  const fetchInterviews = async (filterParams = {}) => {
    setLoading(true)
    clearError()

    try {
      // Merge current filters with new parameters
      const params = {
        ...filters.value,
        ...filterParams
      }

      // Remove null values from params
      Object.keys(params).forEach(key => {
        if (params[key] === null || params[key] === '') {
          delete params[key]
        }
      })

      const response = await apiClient.getInterviews(params)

      interviews.value = response.data.interviews
      pagination.value = {
        total: response.data.total,
        page: response.data.page,
        per_page: response.data.per_page,
        total_pages: response.data.total_pages
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching interviews'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const fetchInterviewById = async (id) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.getInterview(id)
      currentInterview.value = response.data
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const createInterview = async (interviewData) => {
    setLoading(true)
    clearError()

    try {
      console.log('Creating interview with data:', interviewData)
      const response = await apiClient.createInterview(interviewData)
      console.log('Interview created successfully:', response.data)

      // Add new interview to the list (at the beginning)
      interviews.value.unshift(response.data)

      // Update pagination total
      pagination.value.total += 1

      // Reset to first page if needed
      if (pagination.value.page > 1) {
        pagination.value.page = 1
      }

      return response.data
    } catch (err) {
      console.error('Error creating interview:', err)
      console.error('Error response:', err.response?.data)
      const errorMessage = err.response?.data?.detail || 'Error creating interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const updateInterview = async (id, interviewData) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.updateInterview(id, interviewData)

      // Update interview in the list
      const index = interviews.value.findIndex(interview => interview.id === id)
      if (index !== -1) {
        interviews.value[index] = response.data
      }

      // Update current interview if it's the same
      if (currentInterview.value?.id === id) {
        currentInterview.value = response.data
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error updating interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const deleteInterview = async (id) => {
    setLoading(true)
    clearError()

    try {
      await apiClient.deleteInterview(id)

      // Remove interview from the list
      const index = interviews.value.findIndex(interview => interview.id === id)
      if (index !== -1) {
        interviews.value.splice(index, 1)
        pagination.value.total -= 1
      }

      // Clear current interview if it's the deleted one
      if (currentInterview.value?.id === id) {
        currentInterview.value = null
      }

      return true
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error deleting interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const startInterview = async (id) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.startInterview(id)

      // Update interview in the list
      const index = interviews.value.findIndex(interview => interview.id === id)
      if (index !== -1) {
        interviews.value[index] = response.data
      }

      // Update current interview if it's the same
      if (currentInterview.value?.id === id) {
        currentInterview.value = response.data
        interviewWithFeedback.value = response.data
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error starting interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const completeInterview = async (id, transcriptContent) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.completeInterview(id, {
        transcript_content: transcriptContent
      })

      // Update interview in the list
      const index = interviews.value.findIndex(interview => interview.id === id)
      if (index !== -1) {
        interviews.value[index] = response.data
      }

      // Update current interview if it's the same
      if (currentInterview.value?.id === id) {
        currentInterview.value = response.data
        interviewWithFeedback.value = response.data
      }

      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error completing interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const accessInterviewByLink = async (link) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.getInterviewByLink(link)
      interviewWithFeedback.value = response.data
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error accessing interview'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getInterviewFeedback = async (id) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.getInterviewFeedback(id)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching feedback'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const getInterviewTranscript = async (id) => {
    setLoading(true)
    clearError()

    try {
      const response = await apiClient.getInterviewTranscript(id)
      return response.data
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching transcript'
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
      analyst_id: null,
      candidate_id: null,
      role_id: null,
      client_id: null,
      status_id: null,
      scheduled_from: null,
      scheduled_to: null
    }
  }

  const setCurrentInterview = (interview) => {
    currentInterview.value = interview
  }

  const clearCurrentInterview = () => {
    currentInterview.value = null
  }

  const clearInterviewWithFeedback = () => {
    interviewWithFeedback.value = null
  }

  // Pagination helpers
  const goToPage = async (page) => {
    await fetchInterviews({ page })
  }

  const changePageSize = async (per_page) => {
    await fetchInterviews({ page: 1, per_page })
  }

  // Utility functions
  const copyInterviewLink = (interview) => {
    if (interview.interview_link) {
      const fullUrl = `${window.location.origin}/interview/${interview.interview_link}`
      navigator.clipboard.writeText(fullUrl)
      return fullUrl
    }
    return null
  }

  const getInterviewStatusColor = (status) => {
    const statusColors = {
      'Registered': 'bg-blue-100 text-blue-800',
      'Scheduled': 'bg-yellow-100 text-yellow-800',
      'In Progress': 'bg-purple-100 text-purple-800',
      'Completed': 'bg-green-100 text-green-800',
      'Cancelled': 'bg-red-100 text-red-800',
      'No Show': 'bg-gray-100 text-gray-800'
    }
    return statusColors[status] || 'bg-gray-100 text-gray-800'
  }

  const formatInterviewDate = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (error) {
      return dateString
    }
  }

  return {
    // State
    interviews,
    currentInterview,
    interviewWithFeedback,
    loading,
    error,
    pagination,
    filters,

    // Getters
    activeInterviews,
    totalInterviews,
    interviewsByStatus,

    // Actions
    fetchInterviews,
    fetchInterviewById,
    createInterview,
    updateInterview,
    deleteInterview,
    startInterview,
    completeInterview,
    accessInterviewByLink,
    getInterviewFeedback,
    getInterviewTranscript,
    setFilters,
    resetFilters,
    setCurrentInterview,
    clearCurrentInterview,
    clearInterviewWithFeedback,
    clearError,
    goToPage,
    changePageSize,

    // Utilities
    copyInterviewLink,
    getInterviewStatusColor,
    formatInterviewDate
  }
})
