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
      <div ref="messagesContainer" class="h-96 overflow-y-auto space-y-4 p-2">
        <!-- Loading Messages State -->
        <div v-if="loadingMessages" class="flex justify-center items-center h-full">
          <div class="text-center">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto mb-2"></div>
            <p class="text-gray-600 text-sm">Loading messages...</p>
          </div>
        </div>

        <!-- Messages -->
        <div v-else>
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

          <!-- AI Typing Indicator -->
          <div v-if="isAiResponding" class="flex justify-start">
            <div class="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg text-sm max-w-xs lg:max-w-md">
              <div class="flex items-center space-x-2">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
                <span class="text-xs text-gray-600">AI is thinking...</span>
              </div>
            </div>
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
          :disabled="!newMessage.trim() || isAiResponding"
          class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <span v-if="isAiResponding" class="flex items-center space-x-2">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            <span>Sending...</span>
          </span>
          <span v-else>Send</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '@/utils/api.js'

const route = useRoute()

// Parse interview ID from route parameter
// Route: /interview/interview/:id
const interviewId = route.params.id || ''

// State management
const loading = ref(true)
const loadingMessages = ref(false)
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
const messagesContainer = ref(null)

const newMessage = ref('')
const isAiResponding = ref(false) // Track if AI is currently responding

// Auto-scroll to bottom of messages
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

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

    // Start interview chat (send start_interview message)
    await startInterviewChat()

    // Scroll to bottom after loading all messages
    await scrollToBottom()

    error.value = ''
  } catch (err) {
    console.error('Error loading interview data:', err)
    error.value = err.response?.data?.detail || 'Failed to load interview data. Please check the link and try again.'
  } finally {
    loading.value = false
  }
}

// Send start_interview message when component loads
const startInterviewChat = async () => {
  try {
    const response = await apiClient.sendChatMessage(interviewId, 'start_interview')

    // The response now contains conversation_history with filtered messages
    const conversationHistory = response.data.conversation_history || []

    // Map the conversation history to message format
    messages.value = conversationHistory.map(msg => ({
      id: msg.id,
      sender: msg.role === 'candidate' ? 'user' : 'ai', // Map role to sender
      text: msg.content
    }))

    // Scroll to bottom
    await scrollToBottom()
  } catch (error) {
    console.error('Error starting interview chat:', error)
  }
}

// Load data when component mounts
onMounted(() => {
  loadInterviewData()
})

const sendMessage = async () => {
  if (!newMessage.value.trim() || isAiResponding.value) return

  const userMessage = newMessage.value.trim()
  newMessage.value = ''

  try {
    // Set AI responding state
    isAiResponding.value = true

    // Add user message to chat immediately
    messages.value.push({
      id: Date.now(),
      sender: 'user',
      text: userMessage
    })

    // Scroll to show the user message and typing indicator
    await scrollToBottom()

    // Send message to backend and get AI response
    const response = await apiClient.sendChatMessage(interviewId, 'candidate_answer', userMessage)

    // The response now contains last_message with the AI response
    const lastMessage = response.data.last_message

    if (lastMessage) {
      // Add AI response to chat
      messages.value.push({
        id: lastMessage.id,
        sender: 'ai',
        text: lastMessage.content
      })
    } else {
      console.warn('No AI response received from backend')
      messages.value.push({
        id: Date.now(),
        sender: 'ai',
        text: 'I apologize, but I encountered an issue processing your response. Please try again.'
      })
    }

    // Scroll to bottom
    await scrollToBottom()
  } catch (error) {
    console.error('Error sending chat message:', error)

    // Add error message to chat
    messages.value.push({
      id: Date.now(),
      sender: 'ai',
      text: 'I apologize, but I encountered a technical issue. Please try sending your message again.'
    })

    // Re-add the message to input if sending failed
    if (userMessage) {
      newMessage.value = userMessage
    }

    // Scroll to show error message
    await scrollToBottom()
  } finally {
    // Always reset AI responding state
    isAiResponding.value = false
  }
}
</script>
