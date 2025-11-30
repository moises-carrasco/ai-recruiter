<template>
  <div class="filter-controls bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6">
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <!-- Search and Filters Section -->
      <div class="flex flex-col sm:flex-row gap-4 flex-1">
        <!-- Name Search -->
        <div class="flex-1 min-w-0">
          <label for="nameSearch" class="block text-sm font-medium text-gray-700 mb-1">
            Search by Name
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
            </div>
            <input
              id="nameSearch"
              v-model="localFilters.name"
              type="text"
              placeholder="Search candidates by name..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
              @input="debouncedSearch"
            />
          </div>
        </div>

        <!-- Email Search -->
        <div class="flex-1 min-w-0">
          <label for="emailSearch" class="block text-sm font-medium text-gray-700 mb-1">
            Search by Email
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
            </div>
            <input
              id="emailSearch"
              v-model="localFilters.email"
              type="text"
              placeholder="Search by email..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
              @input="debouncedSearch"
            />
          </div>
        </div>

        <!-- Status Filter -->
        <div class="sm:w-48">
          <label for="statusFilter" class="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            id="statusFilter"
            v-model="localFilters.is_active"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            @change="handleFilterChange"
          >
            <option :value="true">Active</option>
            <option :value="false">Inactive</option>
            <option :value="null">All</option>
          </select>
        </div>
      </div>

      <!-- Actions Section -->
      <div class="flex items-center gap-3">
        <!-- Results Count -->
        <div class="text-sm text-gray-600 whitespace-nowrap">
          {{ totalResults }} result{{ totalResults !== 1 ? 's' : '' }}
        </div>

        <!-- Clear Filters -->
        <button
          v-if="hasActiveFilters"
          @click="clearFilters"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-0.5 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
          Clear
        </button>

        <!-- Page Size Selector -->
        <div class="flex items-center gap-2">
          <label for="pageSize" class="text-sm text-gray-700 whitespace-nowrap">
            Per page:
          </label>
          <select
            id="pageSize"
            v-model="localFilters.per_page"
            class="block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
            @change="handlePageSizeChange"
          >
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Active Filters Display -->
    <div v-if="hasActiveFilters" class="mt-4 flex flex-wrap gap-2">
      <span class="text-sm text-gray-600">Active filters:</span>
      
      <span
        v-if="localFilters.name"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
      >
        Name: "{{ localFilters.name }}"
        <button
          @click="clearFilter('name')"
          class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-600 focus:outline-none"
        >
          <svg class="w-2 h-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
            <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
          </svg>
        </button>
      </span>

      <span
        v-if="localFilters.email"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
      >
        Email: "{{ localFilters.email }}"
        <button
          @click="clearFilter('email')"
          class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-600 focus:outline-none"
        >
          <svg class="w-2 h-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
            <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
          </svg>
        </button>
      </span>

      <span
        v-if="localFilters.is_active === false"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
      >
        Status: Inactive
        <button
          @click="clearFilter('is_active')"
          class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-600 focus:outline-none"
        >
          <svg class="w-2 h-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
            <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
          </svg>
        </button>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// Props
const props = defineProps({
  filters: {
    type: Object,
    default: () => ({
      name: '',
      email: '',
      is_active: true,
      page: 1,
      per_page: 20
    })
  },
  totalResults: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['filter-change', 'page-size-change', 'clear-filters'])

// Local state
const localFilters = ref({ ...props.filters })
let searchTimeout = null

// Computed
const hasActiveFilters = computed(() => {
  return localFilters.value.name || 
         localFilters.value.email || 
         localFilters.value.is_active === false
})

// Methods
const debouncedSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  searchTimeout = setTimeout(() => {
    handleFilterChange()
  }, 500) // 500ms delay
}

const handleFilterChange = () => {
  // Reset to page 1 when filters change
  const filtersToEmit = {
    ...localFilters.value,
    page: 1
  }
  
  emit('filter-change', filtersToEmit)
}

const handlePageSizeChange = () => {
  // Reset to page 1 when page size changes
  const filtersToEmit = {
    ...localFilters.value,
    page: 1
  }
  
  emit('page-size-change', filtersToEmit)
}

const clearFilters = () => {
  localFilters.value = {
    name: '',
    email: '',
    is_active: true,
    page: 1,
    per_page: localFilters.value.per_page // Keep the current page size
  }
  
  emit('clear-filters', localFilters.value)
}

const clearFilter = (filterKey) => {
  if (filterKey === 'is_active') {
    localFilters.value.is_active = true
  } else {
    localFilters.value[filterKey] = ''
  }
  
  handleFilterChange()
}

// Watchers
watch(() => props.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })

// Cleanup timeout on unmount
onMounted(() => {
  return () => {
    if (searchTimeout) {
      clearTimeout(searchTimeout)
    }
  }
})
</script>
