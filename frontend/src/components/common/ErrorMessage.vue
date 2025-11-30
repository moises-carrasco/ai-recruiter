<template>
  <div class="error-message">
    <!-- TODO: Implement error message component -->
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <span class="block sm:inline">{{ message }}</span>
    </div>
  </div>
</template>

<script setup>
// TODO: Add props for message and error type
defineProps({
  message: {
    type: String,
    required: true
  }
})
</script>
