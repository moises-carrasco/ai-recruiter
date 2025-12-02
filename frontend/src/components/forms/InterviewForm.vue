<template>
  <div class="interview-form bg-white p-6 rounded-lg shadow-md">
    <h3 class="text-lg font-semibold text-gray-900 mb-6">
      {{ isEditMode ? 'Edit Interview' : 'New Interview' }}
    </h3>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Analyst Selection -->
      <div>
        <label for="analyst" class="block text-sm font-medium text-gray-700 mb-1">
          Analyst *
        </label>
        <select
          id="analyst"
          v-model="form.analyst_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.analyst_id }"
        >
          <option value="">Select an analyst</option>
          <option
            v-for="analyst in analysts"
            :key="analyst.id"
            :value="analyst.id"
          >
            {{ analyst.first_name }} {{ analyst.last_name }}
          </option>
        </select>
        <p v-if="errors.analyst_id" class="mt-1 text-sm text-red-600">
          {{ errors.analyst_id }}
        </p>
      </div>

      <!-- Candidate Selection -->
      <div>
        <label for="candidate" class="block text-sm font-medium text-gray-700 mb-1">
          Candidate *
        </label>
        <select
          id="candidate"
          v-model="form.candidate_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.candidate_id }"
        >
          <option value="">Select a candidate</option>
          <option
            v-for="candidate in candidates"
            :key="candidate.id"
            :value="candidate.id"
          >
            {{ candidate.first_name }} {{ candidate.last_name }} ({{ candidate.email }})
          </option>
        </select>
        <p v-if="errors.candidate_id" class="mt-1 text-sm text-red-600">
          {{ errors.candidate_id }}
        </p>
      </div>

      <!-- Role Selection -->
      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 mb-1">
          Role *
        </label>
        <select
          id="role"
          v-model="form.role_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.role_id }"
        >
          <option value="">Select a role</option>
          <option
            v-for="role in roles"
            :key="role.id"
            :value="role.id"
          >
            {{ role.text_value }}
          </option>
        </select>
        <p v-if="errors.role_id" class="mt-1 text-sm text-red-600">
          {{ errors.role_id }}
        </p>
      </div>

      <!-- Seniority Selection -->
      <div>
        <label for="seniority" class="block text-sm font-medium text-gray-700 mb-1">
          Seniority *
        </label>
        <select
          id="seniority"
          v-model="form.seniority_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.seniority_id }"
        >
          <option value="">Select seniority level</option>
          <option
            v-for="seniority in seniorities"
            :key="seniority.id"
            :value="seniority.id"
          >
            {{ seniority.text_value }}
          </option>
        </select>
        <p v-if="errors.seniority_id" class="mt-1 text-sm text-red-600">
          {{ errors.seniority_id }}
        </p>
      </div>

      <!-- Client Selection -->
      <div>
        <label for="client" class="block text-sm font-medium text-gray-700 mb-1">
          Client *
        </label>
        <select
          id="client"
          v-model="form.client_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.client_id }"
        >
          <option value="">Select a client</option>
          <option
            v-for="client in clients"
            :key="client.id"
            :value="client.id"
          >
            {{ client.text_value }}
          </option>
        </select>
        <p v-if="errors.client_id" class="mt-1 text-sm text-red-600">
          {{ errors.client_id }}
        </p>
      </div>

      <!-- Scheduled DateTime -->
      <div>
        <label for="scheduledDateTime" class="block text-sm font-medium text-gray-700 mb-1">
          Scheduled Date & Time *
        </label>
        <input
          id="scheduledDateTime"
          v-model="form.scheduled_datetime"
          type="datetime-local"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.scheduled_datetime }"
          :min="minDateTime"
        />
        <p v-if="errors.scheduled_datetime" class="mt-1 text-sm text-red-600">
          {{ errors.scheduled_datetime }}
        </p>
      </div>

      <!-- Status Selection -->
      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
          Status *
        </label>
        <select
          id="status"
          v-model="form.status_id"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.status_id }"
        >
          <option value="">Select status</option>
          <option
            v-for="status in interviewStatuses"
            :key="status.id"
            :value="status.id"
          >
            {{ status.text_value }}
          </option>
        </select>
        <p v-if="errors.status_id" class="mt-1 text-sm text-red-600">
          {{ errors.status_id }}
        </p>
      </div>

      <!-- CV File Upload -->
      <div>
        <label for="cvFile" class="block text-sm font-medium text-gray-700 mb-1">
          CV File
        </label>
        <input
          id="cvFile"
          ref="cvFileInput"
          type="file"
          accept=".txt,.md"
          @change="handleCvFileChange"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <p class="mt-1 text-sm text-gray-500">Accepted formats: TXT, MD (max 10MB)</p>
        <p v-if="cvFileName" class="mt-1 text-sm text-green-600">
          Selected: {{ cvFileName }}
        </p>
        <!-- Download link for existing CV file -->
        <div v-if="isEditMode && props.interview?.cv_file_path" class="mt-2">
          <a
            :href="`${api.defaults.baseURL}/interviews/${props.interview.id}/download-cv`"
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm underline"
          >
            Download current CV file
          </a>
        </div>
      </div>

      <!-- Job Description File Upload -->
      <div>
        <label for="jobDescriptionFile" class="block text-sm font-medium text-gray-700 mb-1">
          Job Description File
        </label>
        <input
          id="jobDescriptionFile"
          ref="jobDescriptionFileInput"
          type="file"
          accept=".txt,.md"
          @change="handleJobDescriptionFileChange"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <p class="mt-1 text-sm text-gray-500">Accepted formats: TXT, MD (max 10MB)</p>
        <p v-if="jobDescriptionFileName" class="mt-1 text-sm text-green-600">
          Selected: {{ jobDescriptionFileName }}
        </p>
        <!-- Download link for existing job description file -->
        <div v-if="isEditMode && props.interview?.job_description_path" class="mt-2">
          <a
            :href="`${api.defaults.baseURL}/interviews/${props.interview.id}/download-job-description`"
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm underline"
          >
            Download current job description file
          </a>
        </div>
      </div>

      <!-- Interview Guidelines -->
      <div>
        <label for="guidelines" class="block text-sm font-medium text-gray-700 mb-1">
          Interview Guidelines
        </label>
        <textarea
          id="guidelines"
          v-model="form.interview_guidelines"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter specific guidelines for the interview..."
        ></textarea>
      </div>

      <!-- Notes -->
      <div>
        <label for="notes" class="block text-sm font-medium text-gray-700 mb-1">
          Notes
        </label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="3"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Additional notes..."
        ></textarea>
      </div>

      <!-- Form Actions -->
      <div class="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          @click="handleCancel"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="loading || !isFormValid"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Saving...
          </span>
          <span v-else>
            {{ isEditMode ? 'Update' : 'Create' }}
          </span>
        </button>
      </div>
    </form>

    <!-- Error Message -->
    <div v-if="submitError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
      <p class="text-sm text-red-600">{{ submitError }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useCandidatesStore } from '../../store/candidates'
import { useUsersStore } from '../../store/users'
import { useLookupStore } from '../../store/lookup'
import api from '../../utils/api'

// Props
const props = defineProps({
  interview: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['save', 'cancel'])

// Stores
const candidatesStore = useCandidatesStore()
const usersStore = useUsersStore()
const lookupStore = useLookupStore()

// Form state
const form = ref({
  analyst_id: '',
  candidate_id: '',
  role_id: '',
  seniority_id: '',
  client_id: '',
  scheduled_datetime: '',
  status_id: '',
  cv_file_path: '',
  job_description_path: '',
  interview_guidelines: '',
  notes: ''
})

const errors = ref({})
const submitError = ref('')
const cvFileName = ref('')
const jobDescriptionFileName = ref('')
const cvFileInput = ref(null)
const jobDescriptionFileInput = ref(null)
const pendingCvFile = ref(null)
const pendingJobDescriptionFile = ref(null)

// Mock data is now handled by the stores directly

// Computed
const isEditMode = computed(() => !!props.interview)

const isFormValid = computed(() => {
  return form.value.analyst_id &&
         form.value.candidate_id &&
         form.value.role_id &&
         form.value.seniority_id &&
         form.value.client_id &&
         form.value.scheduled_datetime &&
         form.value.status_id &&
         Object.keys(errors.value).length === 0
})

const analysts = computed(() => {
  return usersStore.users?.filter(user => user.role === 'analyst') || []
})

const candidates = computed(() => {
  return candidatesStore.candidates || []
})

const roles = computed(() => lookupStore.roles || [])

const seniorities = computed(() => lookupStore.seniorities || [])

const clients = computed(() => lookupStore.clients || [])

const interviewStatuses = computed(() => lookupStore.interviewStatuses || [])

const minDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 30) // At least 30 minutes from now
  return now.toISOString().slice(0, 16)
})

// Methods
const validateField = (field, value) => {
  switch (field) {
    case 'analyst_id':
      if (!value) {
        errors.value.analyst_id = 'Analyst selection is required'
      } else {
        delete errors.value.analyst_id
      }
      break

    case 'candidate_id':
      if (!value) {
        errors.value.candidate_id = 'Candidate selection is required'
      } else {
        delete errors.value.candidate_id
      }
      break

    case 'role_id':
      if (!value) {
        errors.value.role_id = 'Role selection is required'
      } else {
        delete errors.value.role_id
      }
      break

    case 'seniority_id':
      if (!value) {
        errors.value.seniority_id = 'Seniority selection is required'
      } else {
        delete errors.value.seniority_id
      }
      break

    case 'client_id':
      if (!value) {
        errors.value.client_id = 'Client selection is required'
      } else {
        delete errors.value.client_id
      }
      break

    case 'scheduled_datetime':
      if (!value) {
        errors.value.scheduled_datetime = 'Scheduled date and time is required'
      } else {
        const selectedDate = new Date(value)
        const minDate = new Date(minDateTime.value)
        if (selectedDate < minDate) {
          errors.value.scheduled_datetime = 'Interview must be scheduled at least 30 minutes from now'
        } else {
          delete errors.value.scheduled_datetime
        }
      }
      break

    case 'status_id':
      if (!value) {
        errors.value.status_id = 'Status selection is required'
      } else {
        delete errors.value.status_id
      }
      break
  }
}

const validateForm = () => {
  validateField('analyst_id', form.value.analyst_id)
  validateField('candidate_id', form.value.candidate_id)
  validateField('role_id', form.value.role_id)
  validateField('seniority_id', form.value.seniority_id)
  validateField('client_id', form.value.client_id)
  validateField('scheduled_datetime', form.value.scheduled_datetime)
  validateField('status_id', form.value.status_id)
}

const showMessage = (message, type = 'error') => {
  console[type === 'error' ? 'error' : 'log'](message)
  // For now, just log. In a real app, you might show a toast notification
}

const resetForm = () => {
  form.value = {
    analyst_id: '',
    candidate_id: '',
    role_id: '',
    seniority_id: '',
    client_id: '',
    scheduled_datetime: '',
    status_id: '',
    cv_file_path: '',
    job_description_path: '',
    interview_guidelines: '',
    notes: ''
  }
  cvFileName.value = ''
  jobDescriptionFileName.value = ''
  errors.value = {}
  submitError.value = ''
}

const loadInterviewData = () => {
  if (props.interview) {
    form.value = {
      analyst_id: props.interview.analyst_id || '',
      candidate_id: props.interview.candidate_id || '',
      role_id: props.interview.role_id || '',
      seniority_id: props.interview.seniority_id || '',
      client_id: props.interview.client_id || '',
      scheduled_datetime: props.interview.scheduled_datetime ?
        new Date(props.interview.scheduled_datetime).toISOString().slice(0, 16) : '',
      status_id: props.interview.status_id || '',
      cv_file_path: props.interview.cv_file_path || '',
      job_description_path: props.interview.job_description_path || '',
      interview_guidelines: props.interview.interview_guidelines || '',
      notes: props.interview.notes || ''
    }
  }
}

const handleCvFileChange = async (event) => {
  const file = event.target.files[0]
  if (file) {
    try {
      cvFileName.value = file.name
      // For new interviews, we'll upload after creation
      // For existing interviews, upload immediately
      if (isEditMode.value && props.interview?.id) {
        const formData = new FormData()
        formData.append('file', file)
        const response = await api.post(`/interviews/${props.interview.id}/upload-cv`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        form.value.cv_file_path = response.data.file_path
      } else {
        // Store file temporarily for later upload
        pendingCvFile.value = file
        form.value.cv_file_path = file.name // Temporary placeholder
      }
    } catch (error) {
      console.error('Error uploading CV file:', error)
      showMessage('Error uploading CV file', 'error')
      cvFileName.value = ''
      form.value.cv_file_path = ''
      pendingCvFile.value = null
    }
  } else {
    cvFileName.value = ''
    form.value.cv_file_path = ''
    pendingCvFile.value = null
  }
}

const handleJobDescriptionFileChange = async (event) => {
  const file = event.target.files[0]
  if (file) {
    try {
      jobDescriptionFileName.value = file.name
      // For new interviews, we'll upload after creation
      // For existing interviews, upload immediately
      if (isEditMode.value && props.interview?.id) {
        const formData = new FormData()
        formData.append('file', file)
        const response = await api.post(`/interviews/${props.interview.id}/upload-job-description`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        form.value.job_description_path = response.data.file_path
      } else {
        // Store file temporarily for later upload
        pendingJobDescriptionFile.value = file
        form.value.job_description_path = file.name // Temporary placeholder
      }
    } catch (error) {
      console.error('Error uploading job description file:', error)
      showMessage('Error uploading job description file', 'error')
      jobDescriptionFileName.value = ''
      form.value.job_description_path = ''
      pendingJobDescriptionFile.value = null
    }
  } else {
    jobDescriptionFileName.value = ''
    form.value.job_description_path = ''
    pendingJobDescriptionFile.value = null
  }
}

const handleSubmit = async () => {
  validateForm()

  if (!isFormValid.value) {
    console.error('Form is not valid. Current form state:', form.value)
    console.error('Validation errors:', errors.value)
    return
  }

  submitError.value = ''
  console.log('Form is valid, submitting data...')

  try {
    const interviewData = { ...form.value }
    console.log('Original form data:', interviewData)

    // Convert datetime-local format to ISO string
    if (interviewData.scheduled_datetime) {
      interviewData.scheduled_datetime = new Date(interviewData.scheduled_datetime).toISOString()
    }

    // Remove empty optional fields
    if (!interviewData.cv_file_path) delete interviewData.cv_file_path
    if (!interviewData.job_description_path) delete interviewData.job_description_path
    if (!interviewData.interview_guidelines) delete interviewData.interview_guidelines
    if (!interviewData.notes) delete interviewData.notes

    console.log('Final interview data to emit:', interviewData)
    emit('save', interviewData)

    if (!isEditMode.value) {
      resetForm()
      // Reset file inputs
      if (cvFileInput.value) cvFileInput.value.value = ''
      if (jobDescriptionFileInput.value) jobDescriptionFileInput.value.value = ''
    }
  } catch (error) {
    console.error('Error in form submission:', error)
    submitError.value = error.message || 'An error occurred while saving the interview'
  }
}

const handleCancel = () => {
  resetForm()
  emit('cancel')
}

// Watchers
watch(() => form.value.analyst_id, (value) => validateField('analyst_id', value))
watch(() => form.value.candidate_id, (value) => validateField('candidate_id', value))
watch(() => form.value.role_id, (value) => validateField('role_id', value))
watch(() => form.value.seniority_id, (value) => validateField('seniority_id', value))
watch(() => form.value.client_id, (value) => validateField('client_id', value))
watch(() => form.value.scheduled_datetime, (value) => validateField('scheduled_datetime', value))
watch(() => form.value.status_id, (value) => validateField('status_id', value))

watch(() => props.interview, () => {
  loadInterviewData()
}, { immediate: true })

// Lifecycle
onMounted(async () => {
  loadInterviewData()

  // Load lookup data if not already loaded
  if (!lookupStore.roles.length) {
    await lookupStore.fetchLookupData()
  }

  // Load candidates if not already loaded
  if (!candidatesStore.candidates.length) {
    await candidatesStore.fetchCandidates()
  }

  // Load users for analysts if not already loaded
  if (!usersStore.users || !usersStore.users.length) {
    await usersStore.fetchUsers()
  }
})
</script>
