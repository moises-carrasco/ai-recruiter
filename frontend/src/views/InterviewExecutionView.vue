<template>
  <div class="interview-execution max-w-6xl mx-auto space-y-6">
    <!-- Top Section: Interview Metadata -->
    <div class="bg-white shadow-sm rounded-lg p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Interview Details</h2>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span class="ml-3 text-gray-600">Loading interview details...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-500 mb-2">
          <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Failed to Load Interview</h3>
        <p class="text-gray-600">{{ error }}</p>
      </div>

      <!-- Interview Data -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Candidate Name</label>
          <p class="text-base font-semibold text-gray-900">{{ interviewData.candidateName }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Interviewer Name</label>
          <p class="text-base font-semibold text-gray-900">{{ interviewData.interviewerName }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Date & Time</label>
          <p class="text-base font-semibold text-gray-900">{{ interviewData.dateTime }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Role</label>
          <p class="text-base font-semibold text-gray-900">{{ interviewData.role }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Seniority</label>
          <p class="text-base font-semibold text-gray-900">{{ interviewData.seniority }}</p>
        </div>
        <div>
          <label class="text-xs text-gray-500 uppercase tracking-wide block mb-1">Current Status</label>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {{ interviewData.status }}
          </span>
        </div>
      </div>
    </div>

    <!-- Middle Section: Conversation Area -->
    <div class="bg-white shadow-sm rounded-lg p-6 flex-1 min-h-0">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Interview Conversation</h3>
      <div class="h-96 overflow-y-auto space-y-4 p-2">
        <div
          v-for="message in messages"
          :key="message.id"
          class="flex"
          :class="{ 'justify-end': message.sender === 'user', 'justify-start': message.sender === 'ai' }"
        >
          <div
            class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg text-sm"
            :class="message.sender === 'ai' ? 'bg-gray-100 text-gray-900' : 'bg-blue-500 text-white'"
          >
            <p class="whitespace-pre-wrap">{{ message.text }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Section: Input Area -->
    <div class="bg-white shadow-sm rounded-lg p-4">
      <div class="flex space-x-4">
        <textarea
          v-model="newMessage"
          class="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows="3"
          placeholder="Type your response..."
          @keydown.enter.exact.prevent="sendMessage"
        ></textarea>
        <button
          @click="sendMessage"
          :disabled="!newMessage.trim()"
          class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '@/utils/api.js'

const route = useRoute()

// Parse interview ID from route parameter
// Route: /interview/interview/:id
const interviewId = route.params.id || ''

// State management
const loading = ref(true)
const error = ref('')
const interviewData = ref({
  candidateName: '',
  interviewerName: '',
  dateTime: '',
  role: '',
  seniority: '',
  status: ''
})

// Fake conversation messages
const messages = ref([
  {
    id: 1,
    sender: 'ai',
    text: 'Hello! I\'m your AI interviewer. Let\'s begin with some questions about your experience with data engineering.'
  },
  {
    id: 2,
    sender: 'user',
    text: 'Hi! I\'m ready to start the interview.'
  },
  {
    id: 3,
    sender: 'ai',
    text: 'Great! Can you tell me about your experience working with large datasets and data processing pipelines?'
  },
  {
    id: 4,
    sender: 'user',
    text: 'I have several years of experience working with big data technologies. I\'ve built ETL pipelines using Apache Spark and Airflow, and I\'ve worked with both structured and unstructured data.'
  },
  {
    id: 5,
    sender: 'ai',
    text: 'That sounds impressive. Can you walk me through a specific project where you optimized a data pipeline for performance?'
  }
])

const newMessage = ref('')

// Load interview data from API
const loadInterviewData = async () => {
  if (!interviewId) {
    error.value = 'No interview ID provided'
    loading.value = false
    return
  }

  try {
    // Send only the hash part, backend will add the prefix
    const response = await apiClient.getInterviewByLink(interviewId)
    const interview = response.data

    // Map API response to component data
    interviewData.value = {
      candidateName: interview.candidate_name || 'Unknown Candidate',
      interviewerName: interview.analyst_name || 'Unknown Interviewer',
      dateTime: interview.scheduled_datetime || 'Not scheduled',
      role: interview.role_text || 'Not specified',
      seniority: interview.seniority_text || 'Not specified',
      status: interview.status_text || 'Unknown'
    }

    error.value = ''
  } catch (err) {
    console.error('Error loading interview data:', err)
    error.value = err.response?.data?.detail || 'Failed to load interview data. Please check the link and try again.'
  } finally {
    loading.value = false
  }
}

// Load data when component mounts
onMounted(() => {
  loadInterviewData()
})

const sendMessage = () => {
  if (!newMessage.value.trim()) return

  // Add user message
  messages.value.push({
    id: Date.now(),
    sender: 'user',
    text: newMessage.value.trim()
  })

  const userMessage = newMessage.value.trim()
  newMessage.value = ''

  // Simulate AI response after a short delay
  setTimeout(() => {
    const aiResponses = [
      'Thank you for your detailed response. That gives me a good understanding of your experience.',
      'Interesting approach! Can you elaborate on the challenges you faced?',
      'Good point. How did you handle data quality and validation in that scenario?',
      'That\'s a solid technical foundation. Let\'s discuss some more advanced concepts.',
      'I appreciate your thorough explanation. What tools and frameworks did you find most effective?'
    ]

    const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)]

    messages.value.push({
      id: Date.now() + Math.random(),
      sender: 'ai',
      text: randomResponse
    })
  }, 1000 + Math.random() * 2000) // Random delay between 1-3 seconds
}
</script>
