# UI Reference

## Visual Design Standards

### Design Philosophy
The AI Technical Interview System follows a clean, professional, and accessible design approach that prioritizes usability and clarity. The interface should feel modern yet trustworthy, supporting the serious nature of technical interviews while remaining approachable for all user types.

### Color Palette

#### Application Shell Colors
- **Header Blue:** `rgb(20, 20, 90)` or `#14145A` - Main header background
- **Sidebar White:** `#FFFFFF` - Sidebar background
- **Content Background:** `#F9FAFB` (gray-50) - Main content area background

#### Primary Colors
- **Primary Blue:** `#3B82F6` (blue-500) - Main actions, links, primary buttons
- **Primary Dark:** `#1E40AF` (blue-800) - Hover states, active elements
- **Primary Light:** `#DBEAFE` (blue-100) - Backgrounds, subtle highlights

#### Secondary Colors
- **Success Green:** `#10B981` (emerald-500) - Success states, completed actions
- **Warning Orange:** `#F59E0B` (amber-500) - Warnings, pending states
- **Error Red:** `#EF4444` (red-500) - Errors, destructive actions
- **Info Blue:** `#06B6D4` (cyan-500) - Information, neutral notifications

#### Neutral Colors
- **Gray 900:** `#111827` - Primary text, headings
- **Gray 700:** `#374151` - Secondary text
- **Gray 500:** `#6B7280` - Muted text, placeholders
- **Gray 300:** `#D1D5DB` - Borders, dividers
- **Gray 100:** `#F3F4F6` - Background, subtle sections
- **White:** `#FFFFFF` - Main background, cards

### Typography

#### Font Family
- **Primary:** Inter, system-ui, -apple-system, sans-serif
- **Monospace:** 'Fira Code', 'Courier New', monospace (for code/technical content)

#### Font Scales
- **Heading 1:** `text-4xl` (36px) - Page titles
- **Heading 2:** `text-3xl` (30px) - Section headers
- **Heading 3:** `text-2xl` (24px) - Subsection headers
- **Heading 4:** `text-xl` (20px) - Card titles
- **Body Large:** `text-lg` (18px) - Important body text
- **Body:** `text-base` (16px) - Standard body text
- **Body Small:** `text-sm` (14px) - Secondary information
- **Caption:** `text-xs` (12px) - Labels, metadata

#### Font Weights
- **Bold:** `font-bold` (700) - Headings, emphasis
- **Semibold:** `font-semibold` (600) - Subheadings, important text
- **Medium:** `font-medium` (500) - Labels, navigation
- **Normal:** `font-normal` (400) - Body text
- **Light:** `font-light` (300) - Subtle text (use sparingly)

### Spacing and Layout

#### Spacing Scale (Tailwind)
- **xs:** `space-1` (4px) - Tight spacing
- **sm:** `space-2` (8px) - Small spacing
- **md:** `space-4` (16px) - Standard spacing
- **lg:** `space-6` (24px) - Large spacing
- **xl:** `space-8` (32px) - Extra large spacing
- **2xl:** `space-12` (48px) - Section spacing

#### Container Widths
- **Mobile:** Full width with 16px padding
- **Tablet:** `max-w-4xl` (896px)
- **Desktop:** `max-w-6xl` (1152px)
- **Wide:** `max-w-7xl` (1280px)

#### Grid System
- **12-column grid** for complex layouts
- **Responsive breakpoints:** sm (640px), md (768px), lg (1024px), xl (1280px)

### Component Standards

#### Buttons

**Primary Button:**
```html
<button class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200">
  Primary Action
</button>
```

**Secondary Button:**
```html
<button class="bg-gray-100 hover:bg-gray-200 text-gray-900 font-medium py-2 px-4 rounded-md border border-gray-300 transition-colors duration-200">
  Secondary Action
</button>
```

**Danger Button:**
```html
<button class="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200">
  Delete
</button>
```

**Button Sizes:**
- **Small:** `py-1 px-3 text-sm`
- **Medium:** `py-2 px-4 text-base` (default)
- **Large:** `py-3 px-6 text-lg`

#### Form Elements

**Input Field:**
```html
<div class="mb-4">
  <label class="block text-sm font-medium text-gray-700 mb-2">
    Field Label
  </label>
  <input 
    type="text" 
    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    placeholder="Enter value..."
  >
</div>
```

**Select Dropdown:**
```html
<select class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  <option>Select option...</option>
</select>
```

**Textarea:**
```html
<textarea 
  rows="4" 
  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
  placeholder="Enter description..."
></textarea>
```

#### Cards

**Standard Card:**
```html
<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <h3 class="text-lg font-semibold text-gray-900 mb-2">Card Title</h3>
  <p class="text-gray-600">Card content goes here...</p>
</div>
```

**Interactive Card:**
```html
<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200 cursor-pointer">
  <!-- Card content -->
</div>
```

#### Navigation

**Top Navigation Bar:**
```html
<nav class="bg-white border-b border-gray-200 px-4 py-3">
  <div class="max-w-6xl mx-auto flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <h1 class="text-xl font-bold text-gray-900">Interview System</h1>
    </div>
    <div class="flex items-center space-x-4">
      <!-- Navigation items -->
    </div>
  </div>
</nav>
```

**Sidebar Navigation:**
```html
<aside class="w-64 bg-gray-50 border-r border-gray-200 h-full">
  <nav class="p-4 space-y-2">
    <a href="#" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100">
      <span>Dashboard</span>
    </a>
  </nav>
</aside>
```

#### Tables

**Data Table:**
```html
<div class="overflow-x-auto">
  <table class="min-w-full bg-white border border-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Column Header
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200">
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
          Cell Content
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

#### Status Indicators

**Status Badges:**
```html
<!-- Success -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
  Completed
</span>

<!-- Warning -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
  Pending
</span>

<!-- Error -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
  Failed
</span>
```

#### Loading States

**Spinner:**
```html
<div class="flex items-center justify-center">
  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
</div>
```

**Skeleton Loading:**
```html
<div class="animate-pulse">
  <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

## Application Shell Layout

### Base Application Structure

The application follows a three-section layout with a blue header, white sidebar, and main content area:

```
┌─────────────────────────────────────────────────────────┐
│ Header (Blue #14145A)                                   │
│ App Name/Logo                              User Icon    │
├──────────────┬──────────────────────────────────────────┤
│ Sidebar      │ Main Content Area                        │
│ (White)      │ (Light Gray Background)                  │
│              │                                          │
│ • Interviews │                                          │
│ • Candidates │                                          │
│ • Analytics  │                                          │
│ • Settings   │                                          │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
```

### Application Shell Implementation

**Complete Application Shell:**
```html
<div class="min-h-screen flex flex-col">
  <!-- Header -->
  <header class="h-16 flex items-center justify-between px-6" style="background-color: rgb(20, 20, 90);">
    <!-- Left side - App Name/Logo -->
    <div class="flex items-center">
      <h1 class="text-xl font-bold text-white">Interview System</h1>
      <!-- Alternative with logo -->
      <!-- <img src="/logo.svg" alt="Interview System" class="h-8 w-auto"> -->
    </div>
    
    <!-- Right side - User Menu -->
    <div class="flex items-center">
      <button class="p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-full transition-colors duration-200">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>
  </header>
  
  <div class="flex-1 flex">
    <!-- Sidebar Navigation -->
    <nav class="w-64 bg-white border-r border-gray-200 flex-shrink-0">
      <div class="p-4">
        <ul class="space-y-2">
          <li>
            <a href="/dashboard" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
              </svg>
              Dashboard
            </a>
          </li>
          <li>
            <a href="/interviews" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
              </svg>
              Interviews
            </a>
          </li>
          <li>
            <a href="/candidates" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
              </svg>
              Candidates
            </a>
          </li>
          <li>
            <a href="/analytics" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
              </svg>
              Analytics
            </a>
          </li>
          <li>
            <a href="/settings" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100 transition-colors duration-200">
              <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"></path>
              </svg>
              Settings
            </a>
          </li>
        </ul>
      </div>
    </nav>
    
    <!-- Main Content Area -->
    <main class="flex-1 bg-gray-50 overflow-auto">
      <div class="p-6">
        <!-- Page content goes here -->
        <router-view />
      </div>
    </main>
  </div>
</div>
```

### Navigation States

**Active Navigation Item:**
```html
<a href="/interviews" class="flex items-center px-3 py-2 text-blue-700 bg-blue-50 rounded-md font-medium">
  <svg class="w-5 h-5 mr-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
    <!-- Icon SVG -->
  </svg>
  Interviews
</a>
```

**Navigation Item with Badge:**
```html
<a href="/interviews" class="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-gray-100">
  <svg class="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
    <!-- Icon SVG -->
  </svg>
  <span class="flex-1">Interviews</span>
  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
    3
  </span>
</a>
```

### Responsive Behavior

**Mobile Navigation (Collapsible Sidebar):**
```html
<!-- Mobile: Hidden sidebar with overlay -->
<div class="lg:hidden">
  <!-- Overlay -->
  <div class="fixed inset-0 z-40 bg-gray-600 bg-opacity-75" v-show="sidebarOpen"></div>
  
  <!-- Sidebar -->
  <nav class="fixed inset-y-0 left-0 z-50 w-64 bg-white transform transition-transform duration-300 ease-in-out" 
       :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
    <!-- Sidebar content -->
  </nav>
</div>

<!-- Desktop: Always visible sidebar -->
<nav class="hidden lg:block w-64 bg-white border-r border-gray-200">
  <!-- Sidebar content -->
</nav>
```

**Mobile Header with Menu Button:**
```html
<header class="h-16 flex items-center justify-between px-4 lg:px-6" style="background-color: rgb(20, 20, 90);">
  <div class="flex items-center">
    <!-- Mobile menu button -->
    <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-md mr-3">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
      </svg>
    </button>
    
    <h1 class="text-xl font-bold text-white">Interview System</h1>
  </div>
  
  <!-- User menu -->
  <div class="flex items-center">
    <button class="p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-full">
      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
      </svg>
    </button>
  </div>
</header>
```

## Screen Layout Patterns

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────┐
│ Header (Blue #14145A)                                   │
│ Interview System                           [User Icon]  │
├──────────────┬──────────────────────────────────────────┤
│ Sidebar      │ Main Content Area (Gray Background)      │
│ (White)      │                                          │
│              │ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
│ • Dashboard  │ │ Metric  │ │ Metric  │ │ Metric  │     │
│ • Interviews │ │ Card    │ │ Card    │ │ Card    │     │
│ • Candidates │ └─────────┘ └─────────┘ └─────────┘     │
│ • Analytics  │                                          │
│ • Settings   │ ┌─────────────────────────────────────┐ │
│              │ │ Recent Interviews                   │ │
│              │ │ Table/List                          │ │
│              │ │                                     │ │
│              │ └─────────────────────────────────────┘ │
│              │                                          │
│              │ ┌─────────────────────────────────────┐ │
│              │ │ Upcoming Interviews                 │ │
│              │ │ Table/List                          │ │
│              │ │                                     │ │
│              │ └─────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────┘
```

### List View Layout
```
┌─────────────────────────────────────────────────────────┐
│ Header (Blue #14145A)                                   │
│ Interview System                           [User Icon]  │
├──────────────┬──────────────────────────────────────────┤
│ Sidebar      │ Main Content Area (Gray Background)      │
│ (White)      │                                          │
│              │ Page Title                    [+ New]   │
│ • Dashboard  │                                          │
│ • Interviews │ ┌─────────────────────────────────────┐ │
│ • Candidates │ │ Filters: [Role ▼] [Status ▼]       │ │
│ • Analytics  │ │ [Search...              ] [🔍]     │ │
│ • Settings   │ └─────────────────────────────────────┘ │
│              │                                          │
│              │ ┌─────────────────────────────────────┐ │
│              │ │ Data Table                          │ │
│              │ │ ┌─────┬─────────┬─────────┬───────┐ │ │
│              │ │ │ ☐   │ Name    │ Role    │ Act.  │ │ │
│              │ │ ├─────┼─────────┼─────────┼───────┤ │ │
│              │ │ │ ☐   │ John D. │ Dev     │ [E][D]│ │ │
│              │ │ │ ☐   │ Jane S. │ QA      │ [E][D]│ │ │
│              │ │ └─────┴─────────┴─────────┴───────┘ │ │
│              │ └─────────────────────────────────────┘ │
│              │                                          │
│              │ Pagination: [< Prev] [1] [2] [Next >]  │
└──────────────┴──────────────────────────────────────────┘
```

### Form Layout
```
┌─────────────────────────────────────────────────────────┐
│ Header (Blue #14145A)                                   │
│ Interview System                           [User Icon]  │
├──────────────┬──────────────────────────────────────────┤
│ Sidebar      │ Main Content Area (Gray Background)      │
│ (White)      │                                          │
│              │ ← Back to List                          │
│ • Dashboard  │                                          │
│ • Interviews │ Form Title                              │
│ • Candidates │                                          │
│ • Analytics  │ ┌─────────────────────────────────────┐ │
│ • Settings   │ │ ┌─────────────┐ ┌─────────────────┐ │ │
│              │ │ │ First Name  │ │ Last Name       │ │ │
│              │ │ │ [Input    ] │ │ [Input        ] │ │ │
│              │ │ └─────────────┘ └─────────────────┘ │ │
│              │ │                                     │ │
│              │ │ ┌─────────────────────────────────┐ │ │
│              │ │ │ Email Address                   │ │ │
│              │ │ │ [Input Field              ]     │ │ │
│              │ │ └─────────────────────────────────┘ │ │
│              │ │                                     │ │
│              │ │ ┌─────────────────────────────────┐ │ │
│              │ │ │ Description                     │ │ │
│              │ │ │ [Text Area                    ] │ │ │
│              │ │ │ [                             ] │ │ │
│              │ │ └─────────────────────────────────┘ │ │
│              │ │                                     │ │
│              │ │ [Cancel] [Save Draft] [Save]        │ │
│              │ └─────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────┘
```

### Interview Detail Layout
```
┌─────────────────────────────────────────────────────────┐
│ Header (Blue #14145A)                                   │
│ Interview System                           [User Icon]  │
├──────────────┬──────────────────────────────────────────┤
│ Sidebar      │ Main Content Area (Gray Background)      │
│ (White)      │                                          │
│              │ ← Back to Interviews                    │
│ • Dashboard  │                                          │
│ • Interviews │ Interview with John Doe                 │
│ • Candidates │                                          │
│ • Analytics  │ ┌─────────────────────────────────────┐ │
│ • Settings   │ │ Status Timeline                     │ │
│              │ │ [●]──────[●]──────[○]               │ │
│              │ │ Scheduled In Progress Completed     │ │
│              │ └─────────────────────────────────────┘ │
│              │                                          │
│              │ ┌─────────────┐ ┌─────────────────────┐ │
│              │ │ Candidate   │ │ Interview Details   │ │
│              │ │ Info        │ │                     │ │
│              │ │             │ │ Date: 2024-01-15    │ │
│              │ │ John Doe    │ │ Time: 10:00 AM      │ │
│              │ │ Senior Dev  │ │ Duration: 60 min    │ │
│              │ │             │ │ Type: Technical     │ │
│              │ └─────────────┘ └─────────────────────┘ │
│              │                                          │
│              │ ┌─────────────────────────────────────┐ │
│              │ │ Feedback & Results                  │ │
│              │ │ Overall Score: 4.2/5                │ │
│              │ │ [Progress bars for skills]          │ │
│              │ └─────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────┘
```

## Responsive Design Guidelines

### Mobile First Approach
- Design for mobile screens first (320px+)
- Progressive enhancement for larger screens
- Touch-friendly interface elements (minimum 44px touch targets)
- Simplified navigation for mobile devices

### Breakpoint Strategy
- **Mobile:** 320px - 639px (single column, stacked layout)
- **Tablet:** 640px - 1023px (two-column layout, condensed navigation)
- **Desktop:** 1024px+ (full layout, sidebar navigation)

### Mobile Adaptations
- **Navigation:** Hamburger menu with slide-out drawer
- **Tables:** Horizontal scroll or card-based layout
- **Forms:** Single column, larger input fields
- **Buttons:** Full-width on mobile, inline on desktop

## Accessibility Standards

### WCAG 2.1 AA Compliance
- **Color Contrast:** Minimum 4.5:1 for normal text, 3:1 for large text
- **Keyboard Navigation:** All interactive elements accessible via keyboard
- **Screen Reader Support:** Proper ARIA labels and semantic HTML
- **Focus Indicators:** Clear visual focus states for all interactive elements

### Implementation Guidelines
- Use semantic HTML elements (`<nav>`, `<main>`, `<section>`, etc.)
- Provide alt text for all images
- Use proper heading hierarchy (h1 → h2 → h3)
- Include skip links for keyboard navigation
- Ensure form labels are properly associated with inputs

## Animation and Transitions

### Transition Standards
- **Duration:** 200ms for hover states, 300ms for layout changes
- **Easing:** `ease-in-out` for most transitions
- **Properties:** Focus on `opacity`, `transform`, and `background-color`

### Animation Guidelines
- **Subtle Animations:** Enhance UX without being distracting
- **Loading States:** Smooth transitions between loading and loaded states
- **Hover Effects:** Subtle feedback for interactive elements
- **Page Transitions:** Smooth navigation between views

### Common Animations
```css
/* Fade in */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Slide up */
.slide-up-enter-active, .slide-up-leave-active {
  transition: transform 0.3s ease;
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(20px);
}
```

## User Experience Patterns

### Interview-Specific UI Components

#### Interview Status Timeline
```html
<div class="flex items-center space-x-4">
  <div class="flex items-center">
    <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
      <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
    </div>
    <span class="ml-2 text-sm font-medium text-gray-900">Scheduled</span>
  </div>
  <div class="flex-1 h-0.5 bg-gray-200"></div>
  <div class="flex items-center">
    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
      <span class="text-white text-sm font-medium">2</span>
    </div>
    <span class="ml-2 text-sm font-medium text-blue-600">In Progress</span>
  </div>
  <div class="flex-1 h-0.5 bg-gray-200"></div>
  <div class="flex items-center">
    <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
      <span class="text-gray-600 text-sm font-medium">3</span>
    </div>
    <span class="ml-2 text-sm font-medium text-gray-500">Completed</span>
  </div>
</div>
```

#### Candidate Profile Card
```html
<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <div class="flex items-start space-x-4">
    <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
      <span class="text-blue-600 font-semibold text-lg">JD</span>
    </div>
    <div class="flex-1">
      <h3 class="text-lg font-semibold text-gray-900">John Doe</h3>
      <p class="text-gray-600">john.doe@example.com</p>
      <div class="mt-2 flex items-center space-x-4">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          Senior Developer
        </span>
        <span class="text-sm text-gray-500">5 years experience</span>
      </div>
    </div>
    <div class="flex space-x-2">
      <button class="text-blue-600 hover:text-blue-800">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
        </svg>
      </button>
      <button class="text-gray-400 hover:text-gray-600">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" clip-rule="evenodd"></path>
          <path fill-rule="evenodd" d="M4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 3a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"></path>
        </svg>
      </button>
    </div>
  </div>
</div>
```

#### Interview Feedback Display
```html
<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">Interview Feedback</h3>
  
  <!-- Overall Rating -->
  <div class="mb-6">
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm font-medium text-gray-700">Overall Rating</span>
      <span class="text-2xl font-bold text-blue-600">4.2/5</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div class="bg-blue-500 h-2 rounded-full" style="width: 84%"></div>
    </div>
  </div>
  
  <!-- Skills Breakdown -->
  <div class="space-y-4">
    <div>
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-medium text-gray-700">Python Programming</span>
        <span class="text-sm font-semibold text-gray-900">4/5</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-1.5">
        <div class="bg-green-500 h-1.5 rounded-full" style="width: 80%"></div>
      </div>
    </div>
    <div>
      <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-medium text-gray-700">Database Design</span>
        <span class="text-sm font-semibold text-gray-900">3/5</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-1.5">
        <div class="bg-yellow-500 h-1.5 rounded-full" style="width: 60%"></div>
      </div>
    </div>
  </div>
</div>
```

### Error States and Messages

#### Error Message Component
```html
<div class="rounded-md bg-red-50 p-4 mb-4">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
    </div>
    <div class="ml-3">
      <h3 class="text-sm font-medium text-red-800">Error occurred</h3>
      <div class="mt-2 text-sm text-red-700">
        <p>Unable to save interview. Please check your connection and try again.</p>
      </div>
    </div>
  </div>
</div>
```

#### Success Message Component
```html
<div class="rounded-md bg-green-50 p-4 mb-4">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
    </div>
    <div class="ml-3">
      <h3 class="text-sm font-medium text-green-800">Success</h3>
      <div class="mt-2 text-sm text-green-700">
        <p>Interview has been scheduled successfully.</p>
      </div>
    </div>
  </div>
</div>
```

### Empty States

#### Empty List State
```html
<div class="text-center py-12">
  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
  </svg>
  <h3 class="mt-2 text-sm font-medium text-gray-900">No interviews</h3>
  <p class="mt-1 text-sm text-gray-500">Get started by creating a new interview.</p>
  <div class="mt-6">
    <button class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
      <svg class="-ml-1 mr-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      New Interview
    </button>
  </div>
</div>
```

## Content Guidelines

### Writing Style
- **Tone:** Professional, clear, and helpful
- **Voice:** Active voice preferred over passive
- **Clarity:** Use simple, direct language
- **Consistency:** Maintain consistent terminology throughout

### UI Text Standards

#### Button Labels
- **Primary Actions:** "Save", "Create", "Submit", "Continue"
- **Secondary Actions:** "Cancel", "Back", "Skip"
- **Destructive Actions:** "Delete", "Remove", "Archive"

#### Status Messages
- **Loading:** "Loading...", "Processing...", "Saving..."
- **Success:** "Saved successfully", "Interview created", "Changes applied"
- **Errors:** "Unable to save", "Connection failed", "Invalid input"

#### Form Labels
- Use sentence case: "First name", "Email address"
- Be specific: "Scheduled date and time" vs "Date"
- Include help text when needed: "CV file (PDF, max 10MB)"

### Internationalization Considerations
- Design for text expansion (25-30% longer in other languages)
- Use flexible layouts that accommodate different text lengths
- Avoid text in images
- Consider right-to-left (RTL) language support for future

## Performance Guidelines

### Image Optimization
- Use WebP format when possible
- Provide multiple sizes for responsive images
- Implement lazy loading for images below the fold
- Optimize SVG icons and remove unnecessary metadata

### CSS Performance
- Use Tailwind's purge feature to remove unused styles
- Minimize custom CSS
- Use CSS Grid and Flexbox for layouts
- Avoid complex selectors and deep nesting

### JavaScript Performance
- Implement code splitting for large components
- Use Vue's lazy loading for routes
- Minimize bundle size with tree shaking
- Optimize images and assets

## Browser Support

### Supported Browsers
- **Chrome:** Latest 2 versions
- **Firefox:** Latest 2 versions
- **Safari:** Latest 2 versions
- **Edge:** Latest 2 versions

### Progressive Enhancement
- Core functionality works without JavaScript
- Enhanced features require modern browser support
- Graceful degradation for older browsers
- Polyfills for critical features only

## Implementation Notes

### Tailwind Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}
```

### Vue Component Structure
```vue
<template>
  <div class="component-wrapper">
    <!-- Component content -->
  </div>
</template>

<script setup>
// Component logic
</script>

<style scoped>
/* Component-specific styles (minimal) */
</style>
```

This UI reference provides comprehensive guidelines for maintaining visual consistency and user experience quality throughout the AI Technical Interview System.
