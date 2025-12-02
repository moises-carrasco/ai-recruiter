<template>
  <div class="interview-detail-view">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center space-x-4">
        <button
          @click="goBack"
          class="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Interviews
        </button>
        <div>
          <h1 class="text-3xl font-bold text-gray-900">
            Interview Details
          </h1>
          <p class="mt-2 text-sm text-gray-600">
            View interview information and results
          </p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="flex items-center space-x-2">
        <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="text-gray-600">Loading interview details...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">Error loading interview</h3>
      <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
      <div class="mt-6">
        <button
          @click="loadInterview"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Try Again
        </button>
      </div>
    </div>

    <!-- Interview Details -->
    <div v-else-if="interview" class="space-y-6">
      <!-- Status Timeline -->
      <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Interview Status</h3>
        </div>
        <div class="px-6 py-4">
          <div class="flex items-center justify-center space-x-4">
            <div class="flex items-center">
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center',
                  interview.status_text === 'Registered' || interview.status_text === 'Scheduled' || interview.status_text === 'In Progress' || interview.status_text === 'Completed'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                ]"
              >
                <span class="text-xs font-medium">1</span>
              </div>
              <span class="ml-2 text-sm font-medium text-gray-900">Registered</span>
            </div>
            <div class="flex-1 h-px bg-gray-300"></div>
            <div class="flex items-center">
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center',
                  interview.status_text === 'Scheduled' || interview.status_text === 'In Progress' || interview.status_text === 'Completed'
                    ? 'bg-yellow-500 text-white'
                    : 'bg-gray-300 text-gray-600'
                ]"
              >
                <span class="text-xs font-medium">2</span>
              </div>
              <span class="ml-2 text-sm font-medium text-gray-900">Scheduled</span>
            </div>
            <div class="flex-1 h-px bg-gray-300"></div>
            <div class="flex items-center">
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center',
                  interview.status_text === 'In Progress' || interview.status_text === 'Completed'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                ]"
              >
                <span class="text-xs font-medium">3</span>
              </div>
              <span class="ml-2 text-sm font-medium text-gray-900">In Progress</span>
            </div>
            <div class="flex-1 h-px bg-gray-300"></div>
            <div class="flex items-center">
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center',
                  interview.status_text === 'Completed'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                ]"
              >
                <span class="text-xs font-medium">4</span>
              </div>
              <span class="ml-2 text-sm font-medium text-gray-900">Completed</span>
            </div>
          </div>
          <div class="mt-4 text-center">
            <span
              :class="getStatusColor(interview.status_text)"
              class="inline-flex px-3 py-1 text-sm font-semibold rounded-full"
            >
              {{ interview.status_text }}
            </span>
          </div>
        </div>
      </div>

      <!-- Interview Information -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Candidate Information -->
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">Candidate Information</h3>
          </div>
          <div class="px-6 py-4 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <p class="mt-1 text-sm text-gray-900">{{ interview.candidate_name }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Role</label>
              <p class="mt-1 text-sm text-gray-900">{{ interview.role_text }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Seniority</label>
              <p class="mt-1 text-sm text-gray-900">{{ interview.seniority_text }}</p>
            </div>
            <div v-if="interview.client_text">
              <label class="block text-sm font-medium text-gray-700">Client</label>
              <p class="mt-1 text-sm text-gray-900">{{ interview.client_text }}</p>
            </div>
          </div>
        </div>

        <!-- Interview Details -->
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">Interview Details</h3>
          </div>
          <div class="px-6 py-4 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Analyst</label>
              <p class="mt-1 text-sm text-gray-900">{{ interview.analyst_name }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Scheduled Date & Time</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(interview.scheduled_datetime) }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Created</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(interview.created_at) }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Last Updated</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(interview.updated_at) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Interview Guidelines -->
      <div v-if="interview.interview_guidelines" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Interview Guidelines</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ interview.interview_guidelines }}</p>
        </div>
      </div>

      <!-- Notes -->
      <div v-if="interview.notes" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Notes</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ interview.notes }}</p>
        </div>
      </div>

      <!-- File Downloads -->
      <div v-if="interview.cv_file_path || interview.job_description_path" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Files</h3>
        </div>
        <div class="px-6 py-4">
          <div class="space-y-3">
            <div v-if="interview.cv_file_path" class="flex items-center justify-between">
              <span class="text-sm text-gray-700">CV Document</span>
              <button
                @click="downloadCV"
                class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="-ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download CV
              </button>
            </div>
            <div v-if="interview.job_description_path" class="flex items-center justify-between">
              <span class="text-sm text-gray-700">Job Description</span>
              <button
                @click="downloadJobDescription"
                class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="-ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Job Description
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Section -->
      <div v-if="feedback" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Interview Feedback</h3>
        </div>
        <div class="px-6 py-4 space-y-6">
          <!-- Overall Rating -->
          <div class="flex items-center justify-between">
            <span class="text-lg font-medium text-gray-900">Overall Rating</span>
            <div class="flex items-center space-x-2">
              <div class="text-2xl font-bold text-blue-600">{{ feedback.overall_ranking }}/5</div>
              <div class="flex space-x-1">
                <svg
                  v-for="star in 5"
                  :key="star"
                  :class="[
                    'w-5 h-5',
                    star <= feedback.overall_ranking ? 'text-yellow-400 fill-current' : 'text-gray-300'
                  ]"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Skills Evaluation -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-4">Skills Evaluation</h4>
            <div class="space-y-4">
              <div v-for="skill in feedback.skills_evaluation" :key="skill.skill_name" class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-sm font-medium text-gray-700">{{ skill.skill_name }}</span>
                  <span class="text-sm text-gray-600">{{ skill.ranking }}/5</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    :class="getSkillBarColor(skill.ranking)"
                    class="h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${(skill.ranking / 5) * 100}%` }"
                  ></div>
                </div>
                <p v-if="skill.comments" class="text-sm text-gray-600">{{ skill.comments }}</p>
              </div>
            </div>
          </div>

          <!-- General Comments -->
          <div v-if="feedback.general_comments">
            <h4 class="text-md font-medium text-gray-900 mb-2">General Comments</h4>
            <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ feedback.general_comments }}</p>
          </div>

          <!-- Strengths -->
          <div v-if="feedback.strengths">
            <h4 class="text-md font-medium text-gray-900 mb-2">Strengths</h4>
            <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ feedback.strengths }}</p>
          </div>

          <!-- Areas for Improvement -->
          <div v-if="feedback.areas_for_improvement">
            <h4 class="text-md font-medium text-gray-900 mb-2">Areas for Improvement</h4>
            <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ feedback.areas_for_improvement }}</p>
          </div>

          <!-- Job Fit Assessment -->
          <div v-if="feedback.job_fit_assessment">
            <h4 class="text-md font-medium text-gray-900 mb-2">Job Fit Assessment</h4>
            <p class="text-sm text-gray-700 whitespace-pre-wrap">{{ feedback.job_fit_assessment }}</p>
          </div>
        </div>
      </div>

      <!-- Transcript Section -->
      <div v-if="transcript" class="bg-white shadow-md rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Interview Transcript</h3>
        </div>
        <div class="px-6 py-4">
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <label class="block text-xs font-medium text-gray-500 uppercase">Started At</label>
                <p class="mt-1 text-gray-900">{{ formatDateTime(transcript.started_at) }}</p>
              </div>
              <div v-if="transcript.completed_at">
                <label class="block text-xs font-medium text-gray-500 uppercase">Completed At</label>
                <p class="mt-1 text-gray-900">{{ formatDateTime(transcript.completed_at) }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 uppercase">Duration</label>
                <p class="mt-1 text-gray-900">{{ calculateDuration(transcript.started_at, transcript.completed_at) }}</p>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Transcript Content</label>
              <div class="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                <pre class="text-sm text-gray-900 whitespace-pre-wrap">{{ transcript.transcript_content }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading feedback/transcript -->
      <div v-else-if="interview.status_text === 'Completed' && (loadingFeedback || loadingTranscript)" class="text-center py-8">
        <svg class="animate-spin h-5 w-5 text-blue-600 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="mt-2 text-sm text-gray-600">Loading additional details...</p>
      </div>

      <!-- No feedback yet -->
      <div v-else-if="interview.status_text === 'Completed' && !feedback && !loadingFeedback && !loadingTranscript" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-yellow-800">Feedback not available</h3>
            <p class="mt-1 text-sm text-yellow-700">The interview has been completed, but feedback has not been generated yet.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInterviewsStore } from '../store/interviews'

// Router
const route = useRoute()
const router = useRouter()

// Store
const interviewsStore = useInterviewsStore()

// State
const interview = ref(null)
const feedback = ref(null)
const transcript = ref(null)
const loading = ref(false)
const loadingFeedback = ref(false)
const loadingTranscript = ref(false)
const error = ref(null)

// Computed
const interviewId = computed(() => route.params.id)

// Methods
const loadInterview = async () => {
  if (!interviewId.value) return

  loading.value = true
  error.value = null

  try {
    const interviewData = await interviewsStore.fetchInterviewById(interviewId.value)
    interview.value = interviewData

    // Load feedback and transcript if interview is completed
    if (interviewData.status_text === 'Completed') {
      await loadFeedback()
      await loadTranscript()
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load interview details'
    console.error('Error loading interview:', err)
  } finally {
    loading.value = false
  }
}

const loadFeedback = async () => {
  if (!interviewId.value) return

  loadingFeedback.value = true
  try {
    const feedbackData = await interviewsStore.getInterviewFeedback(interviewId.value)
    feedback.value = feedbackData
  } catch (err) {
    // Feedback not available yet, which is ok
    console.log('Feedback not available:', err.response?.status)
  } finally {
    loadingFeedback.value = false
  }
}

const loadTranscript = async () => {
  if (!interviewId.value) return

  loadingTranscript.value = true
  try {
    const transcriptData = await interviewsStore.getInterviewTranscript(interviewId.value)
    transcript.value = transcriptData
  } catch (err) {
    // Transcript not available yet, which is ok
    console.log('Transcript not available:', err.response?.status)
  } finally {
    loadingTranscript.value = false
  }
}

const goBack = () => {
  router.push('/interviews')
}

const getStatusColor = (status) => {
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

const getSkillBarColor = (ranking) => {
  if (ranking >= 4) return 'bg-green-500'
  if (ranking >= 3) return 'bg-yellow-500'
  if (ranking >= 2) return 'bg-orange-500'
  return 'bg-red-500'
}

const formatDateTime = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (error) {
    return dateString
  }
}

const calculateDuration = (startTime, endTime) => {
  if (!startTime || !endTime) return 'N/A'

  try {
    const start = new Date(startTime)
    const end = new Date(endTime)
    const diffMs = end - start
    const diffMins = Math.floor(diffMs / 60000)

    if (diffMins < 60) {
      return `${diffMins} minute${diffMins !== 1 ? 's' : ''}`
    } else {
      const hours = Math.floor(diffMins / 60)
      const mins = diffMins % 60
      return `${hours} hour${hours !== 1 ? 's' : ''} ${mins} minute${mins !== 1 ? 's' : ''}`
    }
  } catch (error) {
    return 'N/A'
  }
}

const downloadCV = async () => {
  if (!interview.value?.cv_file_path) return

  try {
    // Create download link
    const link = document.createElement('a')
    link.href = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1/interviews/${interview.value.id}/download-cv`
    link.download = `cv_interview_${interview.value.id}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    console.error('Error downloading CV:', err)
    // Fallback: open in new tab
    window.open(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1/interviews/${interview.value.id}/download-cv`, '_blank')
  }
}

const downloadJobDescription = async () => {
  if (!interview.value?.job_description_path) return

  try {
    // Create download link
    const link = document.createElement('a')
    link.href = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1/interviews/${interview.value.id}/download-job-description`
    link.download = `job_description_interview_${interview.value.id}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    console.error('Error downloading job description:', err)
    // Fallback: open in new tab
    window.open(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1/interviews/${interview.value.id}/download-job-description`, '_blank')
  }
}

// Lifecycle
onMounted(async () => {
  await loadInterview()
})
</script>
