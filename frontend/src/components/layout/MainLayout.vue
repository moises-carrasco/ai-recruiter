<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <AppHeader @toggle-sidebar="toggleSidebar" />
    
    <div class="flex-1 flex">
      <!-- Sidebar Navigation -->
      <AppSidebar 
        :is-open="sidebarOpen" 
        @close="closeSidebar"
        class="lg:block"
        :class="{ 'hidden': !sidebarOpen }"
      />
      
      <!-- Mobile Overlay -->
      <div 
        v-if="sidebarOpen" 
        class="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
        @click="closeSidebar"
      ></div>
      
      <!-- Main Content Area -->
      <main class="flex-1 bg-gray-50 overflow-auto">
        <div class="p-6">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

// Sidebar state management
const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

// Close sidebar on route change (mobile)
import { useRouter } from 'vue-router'
const router = useRouter()

router.afterEach(() => {
  if (window.innerWidth < 1024) {
    closeSidebar()
  }
})
</script>
