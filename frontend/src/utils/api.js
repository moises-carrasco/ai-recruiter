/**
 * API utility functions for HTTP requests
 */

import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

  // Custom instance for chat messages with longer timeout
  const chatApi = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: 60000, // 60 seconds for chat messages
    headers: {
      'Content-Type': 'application/json'
    }
  })

  // Add auth token interceptor to chatApi
  chatApi.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // API methods
  export const apiClient = {
  // Authentication
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),

  // Candidates
  getCandidates: (params) => api.get('/candidates', { params }),
  createCandidate: (data) => api.post('/candidates', data),
  getCandidate: (id) => api.get(`/candidates/${id}`),
  updateCandidate: (id, data) => api.put(`/candidates/${id}`, data),
  deleteCandidate: (id) => api.delete(`/candidates/${id}`),
  searchCandidatesByName: (name, skip = 0, limit = 100) => 
    api.get('/candidates/search/by-name', { params: { name, skip, limit } }),
  getCandidateByEmail: (email) => api.get(`/candidates/email/${email}`),

  // Interviews
  getInterviews: (params) => api.get('/interviews/', { params }),
  getInterview: (id) => api.get(`/interviews/${id}/`),
  createInterview: (data) => api.post('/interviews/', data),
  updateInterview: (id, data) => api.put(`/interviews/${id}/`, data),
  deleteInterview: (id) => api.delete(`/interviews/${id}/`),
  getInterviewByLink: (link) => api.get(`/interviews/link/${link}/`),
  sendChatMessage: (interviewId, messageType, message = null) => chatApi.post(`/interviews/link/${interviewId}/chat/`, { message_type: messageType, message }),
  getInterviewTranscripts: (interviewId) => api.get(`/interviews/link/${interviewId}/transcripts/`),
  startInterview: (id) => api.post(`/interviews/${id}/start/`),
  completeInterview: (id) => api.post(`/interviews/${id}/complete/`),
  getInterviewFeedback: (id) => api.get(`/interviews/${id}/feedback/`),

  // Lookup data
  getLookupData: () => api.get('/lookup'),
  getRoles: () => api.get('/lookup/roles'),
  getClients: () => api.get('/lookup/clients'),
  getSeniorities: () => api.get('/lookup/seniorities'),
  getInterviewStatuses: () => api.get('/lookup/statuses'),

  // Users
  getUsers: () => api.get('/users'),
  createUser: (data) => api.post('/users', data),
  updateUser: (id, data) => api.put(`/users/${id}`, data),
  deleteUser: (id) => api.delete(`/users/${id}`)
}

export default api
