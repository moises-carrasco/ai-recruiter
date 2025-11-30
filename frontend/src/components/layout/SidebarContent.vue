<template>
  <nav class="p-4">
    <ul class="space-y-2">
      <li>
        <router-link 
          to="/"
          class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200"
          :class="{ 'text-blue-700 bg-blue-50 font-medium': $route.path === '/' }"
        >
          <svg class="w-5 h-5 mr-3" :class="{ 'text-blue-500': $route.path === '/' }" fill="currentColor" viewBox="0 0 20 20">
            <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
          </svg>
          Dashboard
        </router-link>
      </li>
      
      <li>
        <router-link 
          to="/interviews"
          class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200"
          :class="{ 'text-blue-700 bg-blue-50 font-medium': $route.path.startsWith('/interviews') }"
        >
          <svg class="w-5 h-5 mr-3" :class="{ 'text-blue-500': $route.path.startsWith('/interviews') }" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
          </svg>
          <span class="flex-1">Interviews</span>
          <span v-if="pendingInterviews > 0" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
            {{ pendingInterviews }}
          </span>
        </router-link>
      </li>
      
      <li>
        <router-link 
          to="/candidates"
          class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200"
          :class="{ 'text-blue-700 bg-blue-50 font-medium': $route.path.startsWith('/candidates') }"
        >
          <svg class="w-5 h-5 mr-3" :class="{ 'text-blue-500': $route.path.startsWith('/candidates') }" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
          </svg>
          Candidates
        </router-link>
      </li>
      
      <li>
        <router-link 
          to="/analytics"
          class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200"
          :class="{ 'text-blue-700 bg-blue-50 font-medium': $route.path.startsWith('/analytics') }"
        >
          <svg class="w-5 h-5 mr-3" :class="{ 'text-blue-500': $route.path.startsWith('/analytics') }" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
          </svg>
          Analytics
        </router-link>
      </li>
      
      <li>
        <router-link 
          to="/settings"
          class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200"
          :class="{ 'text-blue-700 bg-blue-50 font-medium': $route.path.startsWith('/settings') }"
        >
          <svg class="w-5 h-5 mr-3" :class="{ 'text-blue-500': $route.path.startsWith('/settings') }" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
          </svg>
          Settings
        </router-link>
      </li>
    </ul>
    
    <!-- Divider -->
    <hr class="my-4 border-gray-200">
    
    <!-- Additional Actions -->
    <div class="space-y-2">
      <button class="flex items-center w-full px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
        <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
        </svg>
        Help & Support
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Mock data for pending interviews badge
// TODO: Replace with actual data from store
const pendingInterviews = computed(() => {
  return 3 // Mock value
})
</script>
