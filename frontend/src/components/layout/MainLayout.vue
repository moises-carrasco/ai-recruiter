<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <AppHeader @toggle-sidebar="toggleSidebar" />

    <div class="flex-1 flex">
      <!-- Sidebar Navigation - Hidden for interview execution -->
      <AppSidebar
        v-if="!isInterviewExecution"
        :is-open="sidebarOpen"
        @close="closeSidebar"
        class="lg:block"
        :class="{ 'hidden': !sidebarOpen }"
      />

      <!-- Mobile Overlay - Only show when sidebar exists -->
      <div
        v-if="sidebarOpen && !isInterviewExecution"
        class="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
        @click="closeSidebar"
      ></div>

      <!-- Main Content Area -->
      <main :class="isInterviewExecution ? 'flex-1 bg-white overflow-auto' : 'flex-1 bg-gray-50 overflow-auto'">
        <div :class="isInterviewExecution ? 'p-0' : 'p-6'">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

// Router
const route = useRoute()
const router = useRouter()

// Check if current route is interview execution (should hide sidebar and header)
const isInterviewExecution = computed(() => {
  return route.name === 'interview-execution'
})

// Sidebar state management (only used when sidebar is visible)
const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

// Close sidebar on route change (mobile) - only if sidebar exists
router.afterEach(() => {
  if (window.innerWidth < 1024 && !isInterviewExecution.value) {
    closeSidebar()
  }
})
</script>
