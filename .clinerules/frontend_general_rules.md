# Frontend General Rules (Vue 3 + Tailwind + Vite)

These rules define the global frontend conventions for this project.
Cline MUST follow these rules when generating or modifying frontend code.

---

## 1. Project Architecture Principles
- The frontend uses **Vue 3 Composition API**.
- Folder structure must remain:
  - `components/`
  - `views/`
  - `store/`
  - `router/`
  - `utils/`
  - `assets/`
- No business logic inside components; logic belongs in store/services.
- Components must be small, reusable, and stateless when possible.

---

## 2. Code Style & Naming
- Use **PascalCase** for components (`CandidateCard.vue`).
- Use **camelCase** for JS variables and functions.
- Use **kebab-case** for non-Vue filenames.
- Use descriptive, meaningful naming.

---

## 3. Tailwind Usage
- Prefer Tailwind utility classes for styling.
- Avoid inline `style=""` unless absolutely necessary.
- Extract repeated utility patterns into reusable classes if needed.

---

## 4. API Interaction Rules
- All HTTP calls must go through:
  - `utils/api.js` OR
  - service files inside a `/services` folder (if created).
- No direct axios calls inside components.
- All API responses must be validated or sanitized before use.

---

## 5. State Management Rules
- Store must manage:
  - state
  - actions (async operations)
  - getters
- Components should NOT execute async API calls directly.
- Keep store state minimal and consistent.

---

## 6. View Responsibility
- Views represent full screens/pages.
- Views orchestrate components and trigger store actions.
- Views may contain page-level state or logic specific to the page.

---

## 7. Component Responsibility
- Must be reusable and modular.
- Must accept props for dynamic data.
- Must emit events upward instead of mutating parent state.
- Must avoid domain/business logic.

---

## 8. Routing Rules
- All routes must be defined in `router/index.js`.
- Use lazy-loading for views via `() => import("./MyView.vue")`.
- Route paths must be short, lowercase, and descriptive.

---

## 9. Error & Loading States
- All async views must implement:
  - a loading indicator
  - an error state fallback
- UI messages must be human-friendly and clear.

---

## 10. UI/UX Rules
- Follow clean, minimal UI design.
- Maintain consistent spacing using Tailwind utilities.
- Use responsive Tailwind classes (`sm:`, `md:`, `lg:`).
- Avoid deeply nested or overly complex layouts.

---

## 11. SOLID Principles for Frontend
- **Single Responsibility Principle (SRP):**
  - Each component must have one clear purpose and responsibility
  - Views must only orchestrate components and handle page-level logic
  - Store modules must manage state for one specific domain
- **Open/Closed Principle (OCP):**
  - Extend functionality through new components, not modification of existing ones
  - Use composition and props to make components extensible
  - Store actions should be extensible without modifying existing logic
- **Liskov Substitution Principle (LSP):**
  - Component props interfaces must be consistent and interchangeable
  - Store modules must follow consistent patterns for actions and getters
- **Interface Segregation Principle (ISP):**
  - Components should receive only the props they actually need
  - Avoid passing entire objects when only specific properties are required
  - Create focused composables for specific functionality
- **Dependency Inversion Principle (DIP):**
  - Components must depend on store abstractions, not direct API calls
  - High-level views must not depend on low-level component implementations
  - Use dependency injection through provide/inject when needed

---

## 12. Design Pattern Guidelines
- **Composition Pattern (Required):**
  - Prefer component composition over inheritance
  - Build complex UIs by combining simple, focused components
  - Use slots and props for flexible component composition
- **Observer Pattern (Recommended for):**
  - Reactive state management with Vue's reactivity system
  - Event-driven communication between components
  - Real-time updates from backend via store watchers
- **Factory Pattern (Use for):**
  - Dynamic component creation based on data types
  - Form field generation based on schema definitions
  - Creating different UI variants based on user roles
- **Adapter Pattern (Use for):**
  - API response transformation in services layer
  - Legacy component integration
  - Third-party library integration
- **Strategy Pattern (Consider for):**
  - Different validation strategies for forms
  - Multiple layout options for the same data
  - Conditional rendering based on user permissions
