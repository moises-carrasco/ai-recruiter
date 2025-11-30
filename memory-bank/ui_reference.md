# UI Reference

## Visual Design Standards

### Design Philosophy
The AI Technical Interview System follows a clean, professional design approach optimized for desktop use. The interface prioritizes usability and clarity for technical interviews while maintaining a modern appearance.

**Note:** This POC is desktop-focused with minimal mobile support. Mobile optimization will be addressed in future iterations.

### Color Palette

#### Core Colors (POC Essential)
- **Primary Blue:** `#3B82F6` - Main actions, links, primary buttons
- **Gray 900:** `#111827` - Primary text, headings
- **White:** `#FFFFFF` - Main background, cards
- **Success Green:** `#10B981` - Success states, completed actions
- **Error Red:** `#EF4444` - Errors, destructive actions

#### Application Shell Colors
- **Header Blue:** `#14145A` - Main header background
- **Sidebar White:** `#FFFFFF` - Sidebar background
- **Content Background:** `#F9FAFB` - Main content area background

### Typography

#### Font Family
- **Primary:** Inter, system-ui, -apple-system, sans-serif

#### Font Scales (POC Essential)
- **Heading 1:** `text-4xl` (36px) - Page titles
- **Heading 3:** `text-2xl` (24px) - Section headers
- **Body:** `text-base` (16px) - Standard body text
- **Caption:** `text-xs` (12px) - Labels, metadata

#### Font Weights
- **Bold:** `font-bold` (700) - Headings, emphasis
- **Semibold:** `font-semibold` (600) - Subheadings, important text
- **Normal:** `font-normal` (400) - Body text

### Spacing and Layout

#### Spacing Scale (Simplified)
- **Small:** `space-2` (8px) - Tight spacing
- **Medium:** `space-4` (16px) - Standard spacing
- **Large:** `space-8` (32px) - Section spacing

#### Container Widths
- **Desktop:** `max-w-6xl` (1152px) - Primary container width

## Component Standards

### Buttons

#### Primary Button
**Purpose:** Main action in a workflow or form

**Visual Attributes:**
- Background: Primary blue (#3B82F6)
- Text: White, semibold weight
- Padding: Medium (py-2 px-4)
- Border radius: Medium (rounded-md)

**Behavioral Expectations:**
- Used for primary actions like "Save", "Create", "Submit"
- Disabled state: 50% opacity
- Focus state: Visible outline for accessibility

#### Secondary Button
**Purpose:** Alternative or supporting actions

**Visual Attributes:**
- Background: Light gray (#F3F4F6)
- Text: Dark gray (#111827), semibold weight
- Border: Light gray border
- Same padding and radius as primary

**Behavioral Expectations:**
- Used alongside primary buttons for "Cancel", "Back" actions
- Less visual prominence than primary buttons

### Form Elements

#### Input Fields
**Purpose:** Text data collection from users

**Visual Attributes:**
- Full width within container
- Medium padding (px-3 py-2)
- Light gray border
- Rounded corners (rounded-md)
- Focus state: Blue ring (#3B82F6)

**Behavioral Expectations:**
- Clear placeholder text when appropriate
- Proper label association
- Validation feedback through border color changes

#### Select Dropdowns
**Purpose:** Single option selection

**Visual Attributes:**
- Same styling as input fields
- Dropdown arrow indicator
- Options list with hover states

**Behavioral Expectations:**
- Keyboard navigation support
- Clear option text

#### Textarea Fields
**Purpose:** Multi-line text input

**Visual Attributes:**
- Same base styling as inputs
- Minimum height of 4 rows
- Vertical resize capability

**Behavioral Expectations:**
- Auto-resize or scroll for long content
- Proper label association

### Cards

#### Standard Card
**Purpose:** Content grouping and organization

**Visual Attributes:**
- White background
- Subtle shadow (shadow-sm)
- Light border
- Medium padding (p-6)
- Rounded corners (rounded-lg)

**Content Structure:**
- Clear hierarchy with title and content
- Consistent internal spacing
- Logical content flow

### Tables

#### Data Table
**Purpose:** Structured data display

**Visual Structure:**
- White background with borders
- Header row with gray background
- Row hover states
- Responsive horizontal scrolling

**Column Design:**
- Left-aligned text content
- Right-aligned numeric data
- Consistent padding across cells

**Behavioral Expectations:**
- Action buttons in dedicated columns
- Clear column headers

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

### Layout Specifications

#### Header Section
**Purpose:** Application branding and global user actions

**Layout Requirements:**
- Fixed height: 64px (h-16)
- Full width with horizontal padding
- Blue background (#14145A)
- Left: Application name/logo with white text
- Right: User menu

#### Sidebar Section
**Purpose:** Primary navigation for application sections

**Layout Requirements:**
- Fixed width: 256px on desktop
- Full height with white background
- Vertical navigation list
- Border separation from main content

**Navigation Structure:**
- Dashboard
- Interviews
- Candidates
- Analytics
- Settings

#### Main Content Section
**Purpose:** Primary application content display

**Layout Requirements:**
- Flexible width (remaining space)
- Light gray background (#F9FAFB)
- Consistent padding (24px)
- Scrollable content area

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

**Layout Specifications:**
- **Metric Cards:** 3-column grid on desktop
- **Content Sections:** Full-width cards with consistent spacing
- **Spacing:** 24px between major sections

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

**Layout Specifications:**
- **Header Section:** Page title with primary action button
- **Filter Section:** Horizontal filter controls with search
- **Table Section:** Full-width data table with actions
- **Pagination:** Bottom-aligned navigation controls

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

**Layout Specifications:**
- **Navigation:** Back link for context
- **Form Container:** Centered card with proper spacing
- **Field Layout:** Two-column for related fields, full-width for others
- **Actions:** Right-aligned button group

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

**Layout Specifications:**
- **Status Timeline:** Horizontal progress indicator
- **Information Cards:** Two-column layout for related data
- **Results Section:** Full-width feedback display

## Basic Form Layout Guidelines

### Form Structure
**Purpose:** Consistent form organization for data collection

**Layout Principles:**
- Use cards to contain form sections
- Group related fields together
- Provide clear field labels
- Include helpful placeholder text
- Place action buttons at the bottom right

**Field Organization:**
- Two-column layout for related fields (First Name / Last Name)
- Full-width for standalone fields (Email, Description)
- Consistent spacing between field groups
- Clear visual hierarchy

### Error Handling
**Purpose:** Basic user feedback for form validation

**Visual Approach:**
- Red border for invalid fields
- Simple error text below problematic fields
- Success state with green border for valid submission

## Implementation Notes

### Tailwind CSS Classes
This UI reference assumes the use of Tailwind CSS for styling. The mentioned classes (like `py-2`, `px-4`, `rounded-md`, etc.) correspond to Tailwind utility classes.

### Component Consistency
All components should maintain visual consistency across the application:
- Use the defined color palette consistently
- Apply the same spacing rules throughout
- Maintain consistent typography hierarchy
- Follow the established layout patterns

This simplified UI reference provides the essential design guidelines needed for the POC while maintaining clarity and consistency across the AI Technical Interview System.
