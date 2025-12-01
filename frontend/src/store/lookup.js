/**
 * Lookup data store using Pinia
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '../utils/api'

export const useLookupStore = defineStore('lookup', () => {
  // State
  const roles = ref([])
  const clients = ref([])
  const seniorities = ref([])
  const interviewStatuses = ref([])
  const loading = ref(false)
  const error = ref(null)

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

  const fetchLookupData = async () => {
    setLoading(true)
    clearError()

    try {
      // Fetch data from real API endpoints
      const [rolesResponse, clientsResponse, senioritiesResponse, statusesResponse] = await Promise.all([
        apiClient.getRoles(),
        apiClient.getClients(),
        apiClient.getSeniorities(),
        apiClient.getInterviewStatuses()
      ])

      roles.value = rolesResponse.data || []
      clients.value = clientsResponse.data || []
      seniorities.value = senioritiesResponse.data || []
      interviewStatuses.value = statusesResponse.data || []

      return {
        roles: roles.value,
        clients: clients.value,
        seniorities: seniorities.value,
        interviewStatuses: interviewStatuses.value
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Error fetching lookup data'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const fetchAllLookupData = async () => {
    return await fetchLookupData()
  }

  const fetchRoles = async () => {
    if (roles.value.length === 0) {
      await fetchLookupData()
    }
    return roles.value
  }

  const fetchClients = async () => {
    if (clients.value.length === 0) {
      await fetchLookupData()
    }
    return clients.value
  }

  const fetchSeniorities = async () => {
    if (seniorities.value.length === 0) {
      await fetchLookupData()
    }
    return seniorities.value
  }

  const fetchInterviewStatuses = async () => {
    if (interviewStatuses.value.length === 0) {
      await fetchLookupData()
    }
    return interviewStatuses.value
  }

  const createLookupItem = async (domain, itemData) => {
    // TODO: Implement create lookup item
    setError('Create lookup item not implemented yet')
    throw new Error('Create lookup item not implemented yet')
  }

  const updateLookupItem = async (id, itemData) => {
    // TODO: Implement update lookup item
    setError('Update lookup item not implemented yet')
    throw new Error('Update lookup item not implemented yet')
  }

  const deleteLookupItem = async (id, domain) => {
    // TODO: Implement delete lookup item
    setError('Delete lookup item not implemented yet')
    throw new Error('Delete lookup item not implemented yet')
  }

  return {
    roles,
    clients,
    seniorities,
    interviewStatuses,
    loading,
    error,
    fetchLookupData,
    fetchAllLookupData,
    fetchRoles,
    fetchClients,
    fetchSeniorities,
    fetchInterviewStatuses,
    createLookupItem,
    updateLookupItem,
    deleteLookupItem,
    clearError
  }
})
