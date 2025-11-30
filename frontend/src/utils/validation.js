/**
 * Form validation utility functions
 */

// Email validation
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// Required field validation
export const isRequired = (value) => {
  return value !== null && value !== undefined && value.toString().trim() !== ''
}

// Minimum length validation
export const minLength = (value, min) => {
  return value && value.length >= min
}

// Maximum length validation
export const maxLength = (value, max) => {
  return !value || value.length <= max
}

// Password strength validation
export const isStrongPassword = (password) => {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/
  return passwordRegex.test(password)
}

// File type validation
export const isValidFileType = (file, allowedTypes) => {
  return allowedTypes.includes(file.type)
}

// File size validation (size in MB)
export const isValidFileSize = (file, maxSizeMB) => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024
  return file.size <= maxSizeBytes
}

// Date validation (future date)
export const isFutureDate = (date) => {
  const selectedDate = new Date(date)
  const now = new Date()
  return selectedDate > now
}

// Validation error messages
export const validationMessages = {
  required: 'This field is required',
  email: 'Please enter a valid email address',
  minLength: (min) => `Must be at least ${min} characters`,
  maxLength: (max) => `Must be no more than ${max} characters`,
  password: 'Password must be at least 8 characters with uppercase, lowercase, and number',
  fileType: (types) => `File must be one of: ${types.join(', ')}`,
  fileSize: (size) => `File size must be less than ${size}MB`,
  futureDate: 'Date must be in the future'
}

// Form validation helper
export const validateForm = (formData, rules) => {
  const errors = {}
  
  for (const [field, fieldRules] of Object.entries(rules)) {
    const value = formData[field]
    
    for (const rule of fieldRules) {
      if (rule.type === 'required' && !isRequired(value)) {
        errors[field] = validationMessages.required
        break
      }
      
      if (rule.type === 'email' && value && !isValidEmail(value)) {
        errors[field] = validationMessages.email
        break
      }
      
      if (rule.type === 'minLength' && value && !minLength(value, rule.value)) {
        errors[field] = validationMessages.minLength(rule.value)
        break
      }
      
      if (rule.type === 'maxLength' && !maxLength(value, rule.value)) {
        errors[field] = validationMessages.maxLength(rule.value)
        break
      }
      
      if (rule.type === 'password' && value && !isStrongPassword(value)) {
        errors[field] = validationMessages.password
        break
      }
      
      if (rule.type === 'futureDate' && value && !isFutureDate(value)) {
        errors[field] = validationMessages.futureDate
        break
      }
    }
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}
