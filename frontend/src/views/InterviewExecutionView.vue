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
          :class="{ 'justify-end': message.sender === 'user', 'justify-end': message.sender === 'ai' }"
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

// Messages loaded from database
const messages = ref([])

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

    // Load chat messages from database
    await loadChatMessages()

    error.value = ''
  } catch (err) {
    console.error('Error loading interview data:', err)
    error.value = err.response?.data?.detail || 'Failed to load interview data. Please check the link and try again.'
  } finally {
    loading.value = false
  }
}

// Load chat messages from database
const loadChatMessages = async () => {
  try {
    const response = await apiClient.getInterviewTranscripts(interviewId)
    const transcripts = response.data.transcripts

    // Map transcripts to message format and sort by created_at
    messages.value = transcripts
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
      .map(transcript => ({
        id: transcript.id,
        sender: transcript.role === 'candidate' ? 'user' : 'ai', // Map role to sender
        text: transcript.transcript_content
      }))
  } catch (err) {
    console.error('Error loading chat messages:', err)
    // Don't show error for messages loading, just leave empty
  }
}

// Load data when component mounts
onMounted(() => {
  loadInterviewData()
})

const sendMessage = async () => {
  if (!newMessage.value.trim()) return

  const userMessage = newMessage.value.trim()
  newMessage.value = ''

  try {
    // Add user message to chat
    messages.value.push({
      id: Date.now(),
      sender: 'user',
      text: userMessage
    })

    // Send message to backend and get AI response
    const response = await apiClient.sendChatMessage(interviewId, userMessage)
    const aiResponse = response.data.ai_response

    // Add AI response to chat
    messages.value.push({
      id: Date.now() + 1,
      sender: 'ai',
      text: aiResponse
    })
  } catch (error) {
    console.error('Error sending chat message:', error)
    // Re-add the message to input if sending failed
    newMessage.value = userMessage
    // Could add error handling UI here
  }
}
</script>
