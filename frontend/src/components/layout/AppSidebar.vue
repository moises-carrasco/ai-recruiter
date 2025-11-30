<template>
  <div>
    <!-- Desktop Sidebar -->
    <aside class="hidden lg:block w-64 bg-white border-r border-gray-200 flex-shrink-0">
      <SidebarContent />
    </aside>

    <!-- Mobile Sidebar -->
    <aside 
      v-if="isOpen"
      class="fixed inset-y-0 left-0 z-50 w-64 bg-white transform transition-transform duration-300 ease-in-out lg:hidden"
      :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Mobile Close Button -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Navigation</h2>
        <button 
          @click="$emit('close')"
          class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <SidebarContent />
    </aside>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import SidebarContent from './SidebarContent.vue'

// Props
defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

// Emits
defineEmits(['close'])
</script>
