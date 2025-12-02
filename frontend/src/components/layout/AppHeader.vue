<template>
  <header class="h-16 flex items-center justify-between px-4 lg:px-6" style="background-color: rgb(20, 20, 90);">
    <div class="flex items-center">
      <!-- Mobile menu button -->
      <button 
        @click="$emit('toggle-sidebar')" 
        class="lg:hidden p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-md mr-3 transition-colors duration-200"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      
      <!-- App Logo/Title -->
      <h1 class="text-2xl font-bold" style="background: linear-gradient(to right, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Amauta AI</h1>
    </div>
    
    <!-- Right side - User Menu (Hidden for interview execution) -->
    <div v-if="!isInterviewExecution" class="flex items-center">
      <!-- User Profile Dropdown -->
      <div class="relative">
        <button
          @click="toggleUserMenu"
          class="p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-full transition-colors duration-200 flex items-center space-x-2"
        >
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
          </svg>
          <span class="hidden md:block text-sm">{{ currentUser?.name || 'User' }}</span>
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>

        <!-- User Dropdown Menu -->
        <div
          v-if="userMenuOpen"
          class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 border border-gray-200"
        >
          <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
            Profile Settings
          </a>
          <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
            Preferences
          </a>
          <hr class="my-1">
          <button
            @click="handleLogout"
            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// Emits
defineEmits(['toggle-sidebar'])

// Router
const route = useRoute()
const router = useRouter()

// Check if current route is interview execution (should hide user menu)
const isInterviewExecution = computed(() => {
  return route.name === 'interview-execution'
})

// User menu state
const userMenuOpen = ref(false)

// Mock user data - replace with actual auth store
const currentUser = computed(() => {
  return {
    name: 'John Doe',
    email: 'john.doe@example.com',
    role: 'Admin'
  }
})

const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
}

const handleLogout = () => {
  // TODO: Implement actual logout logic with auth store
  console.log('Logging out...')
  userMenuOpen.value = false
  router.push('/login')
}

// Close user menu when clicking outside
const closeUserMenu = (event) => {
  if (!event.target.closest('.relative')) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeUserMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeUserMenu)
})
</script>
