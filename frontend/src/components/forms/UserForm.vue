<template>
  <div class="user-form bg-white p-6 rounded-lg shadow-md">
    <h3 class="text-lg font-semibold text-gray-900 mb-6">
      {{ isEditMode ? 'Edit User' : 'New User' }}
    </h3>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- First Name -->
      <div>
        <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">
          First Name *
        </label>
        <input
          id="firstName"
          v-model="form.first_name"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.first_name }"
          placeholder="Enter first name"
        />
        <p v-if="errors.first_name" class="mt-1 text-sm text-red-600">
          {{ errors.first_name }}
        </p>
      </div>

      <!-- Last Name -->
      <div>
        <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">
          Last Name *
        </label>
        <input
          id="lastName"
          v-model="form.last_name"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.last_name }"
          placeholder="Enter last name"
        />
        <p v-if="errors.last_name" class="mt-1 text-sm text-red-600">
          {{ errors.last_name }}
        </p>
      </div>

      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
          Email *
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.email }"
          placeholder="Enter email address"
        />
        <p v-if="errors.email" class="mt-1 text-sm text-red-600">
          {{ errors.email }}
        </p>
      </div>

      <!-- Role -->
      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 mb-1">
          Role *
        </label>
        <select
          id="role"
          v-model="form.role"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.role }"
        >
          <option value="" disabled>Select a role</option>
          <option value="analyst">Analyst</option>
          <option value="admin">Administrator</option>
        </select>
        <p v-if="errors.role" class="mt-1 text-sm text-red-600">
          {{ errors.role }}
        </p>
      </div>

      <!-- Password (required for new users, optional for edits) -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
          Password {{ isEditMode ? '(leave blank to keep current)' : '*' }}
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          :required="!isEditMode"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.password }"
          :placeholder="isEditMode ? 'Enter new password (optional)' : 'Enter password'"
        />
        <p v-if="errors.password" class="mt-1 text-sm text-red-600">
          {{ errors.password }}
        </p>
      </div>

      <!-- Confirm Password (only when password is provided) -->
      <div v-if="form.password">
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password *
        </label>
        <input
          id="confirmPassword"
          v-model="form.confirmPassword"
          type="password"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.confirmPassword }"
          placeholder="Confirm password"
        />
        <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
          {{ errors.confirmPassword }}
        </p>
      </div>

      <!-- Active Status (only in edit mode) -->
      <div v-if="isEditMode">
        <label class="flex items-center">
          <input
            v-model="form.is_active"
            type="checkbox"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <span class="ml-2 text-sm text-gray-700">Active</span>
        </label>
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

// Props
const props = defineProps({
  user: {
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

// Form state
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  role: '',
  password: '',
  confirmPassword: '',
  is_active: true
})

const errors = ref({})
const submitError = ref('')

// Computed
const isEditMode = computed(() => !!props.user)

const isFormValid = computed(() => {
  const baseValid = form.value.first_name.trim() &&
                   form.value.last_name.trim() &&
                   form.value.email.trim() &&
                   form.value.role &&
                   isValidEmail(form.value.email) &&
                   Object.keys(errors.value).length === 0

  if (!isEditMode.value) {
    // For new users, password is required
    return baseValid && form.value.password && form.value.password.length >= 6
  }

  // For edit mode, password is optional
  if (form.value.password) {
    return baseValid && form.value.password.length >= 6 && form.value.confirmPassword === form.value.password
  }

  return baseValid
})

// Methods
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const validateField = (field, value) => {
  switch (field) {
    case 'first_name':
      if (!value.trim()) {
        errors.value.first_name = 'First name is required'
      } else if (value.length > 100) {
        errors.value.first_name = 'First name must be less than 100 characters'
      } else {
        delete errors.value.first_name
      }
      break

    case 'last_name':
      if (!value.trim()) {
        errors.value.last_name = 'Last name is required'
      } else if (value.length > 100) {
        errors.value.last_name = 'Last name must be less than 100 characters'
      } else {
        delete errors.value.last_name
      }
      break

    case 'email':
      if (!value.trim()) {
        errors.value.email = 'Email is required'
      } else if (!isValidEmail(value)) {
        errors.value.email = 'Please enter a valid email address'
      } else {
        delete errors.value.email
      }
      break

    case 'role':
      if (!value) {
        errors.value.role = 'Role is required'
      } else if (!['admin', 'analyst'].includes(value)) {
        errors.value.role = 'Role must be either Admin or Analyst'
      } else {
        delete errors.value.role
      }
      break

    case 'password':
      if (!isEditMode.value && !value) {
        errors.value.password = 'Password is required'
      } else if (value && value.length < 6) {
        errors.value.password = 'Password must be at least 6 characters'
      } else {
        delete errors.value.password
      }
      break

    case 'confirmPassword':
      if (form.value.password && value !== form.value.password) {
        errors.value.confirmPassword = 'Passwords do not match'
      } else {
        delete errors.value.confirmPassword
      }
      break
  }
}

const validateForm = () => {
  validateField('first_name', form.value.first_name)
  validateField('last_name', form.value.last_name)
  validateField('email', form.value.email)
  validateField('role', form.value.role)
  if (form.value.password || !isEditMode.value) {
    validateField('password', form.value.password)
    if (form.value.password) {
      validateField('confirmPassword', form.value.confirmPassword)
    }
  }
}

const resetForm = () => {
  form.value = {
    first_name: '',
    last_name: '',
    email: '',
    role: '',
    password: '',
    confirmPassword: '',
    is_active: true
  }
  errors.value = {}
  submitError.value = ''
}

const loadUserData = () => {
  if (props.user) {
    form.value = {
      first_name: props.user.first_name || '',
      last_name: props.user.last_name || '',
      email: props.user.email || '',
      role: props.user.role || '',
      password: '',
      confirmPassword: '',
      is_active: props.user.is_active ?? true
    }
  }
}

const handleSubmit = async () => {
  validateForm()

  if (!isFormValid.value) {
    return
  }

  submitError.value = ''

  try {
    const userData = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      email: form.value.email,
      role: form.value.role
    }

    // Only include password if it's provided (for updates, password is optional)
    if (form.value.password) {
      userData.password = form.value.password
    }

    // Include active status for edits
    if (isEditMode.value) {
      userData.is_active = form.value.is_active
    }

    emit('save', userData)

    if (!isEditMode.value) {
      resetForm()
    }
  } catch (error) {
    submitError.value = error.message || 'An error occurred while saving the user'
  }
}

const handleCancel = () => {
  resetForm()
  emit('cancel')
}

// Watchers
watch(() => form.value.first_name, (value) => validateField('first_name', value))
watch(() => form.value.last_name, (value) => validateField('last_name', value))
watch(() => form.value.email, (value) => validateField('email', value))
watch(() => form.value.role, (value) => validateField('role', value))
watch(() => form.value.password, (value) => validateField('password', value))
watch(() => form.value.confirmPassword, (value) => validateField('confirmPassword', value))

// Watch password to show/hide confirm password field
watch(() => form.value.password, (newPassword) => {
  if (!newPassword) {
    form.value.confirmPassword = ''
    delete errors.value.confirmPassword
  }
})

watch(() => props.user, () => {
  loadUserData()
}, { immediate: true })

// Lifecycle
onMounted(() => {
  loadUserData()
})
</script>
