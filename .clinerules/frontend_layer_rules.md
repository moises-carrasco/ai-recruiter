# Frontend Layer-Specific Rules

Rules for components, views, router, store, and services.
Cline MUST follow these conventions when generating frontend code.

---

# ==========================
# 1. Component Rules
# ==========================
- Components must be **reusable** and **modular**.
- Components must:
  - accept props for external data
  - emit events upward for actions
  - use `<script setup>` when possible
  - contain minimal internal state
- No API calls inside components.
- No business logic inside components.

---

# ==========================
# 2. View Rules
# ==========================
- Views orchestrate multiple components.
- Views may contain page-level logic and state.
- Views must fetch initial data via store actions.
- Views must implement:
  - loading state
  - error state
- Views must NOT interact with axios directly.

---

# ==========================
# 3. Store Rules
# ==========================
- The store handles:
  - global/shared state
  - business logic for UI workflows
  - all async API calls
- Stores must:
  - return clean, pre-processed data
  - avoid storing unnecessary fields
- State must be minimal and predictable.
- Actions must be async.

---

# ==========================
# 4. Router Rules
# ==========================
- All routes go in `router/index.js`.
- Use lazy-loading for views via dynamic imports.
- Paths must be simple and human-readable.
- No logical operations inside route definitions.
- Use nested routes only when appropriate.

---

# ==========================
# 5. Services / API Utilities
# ==========================
- All axios logic must be centralized in:
  - `utils/api.js` OR
  - `/services/*.js`
- Services must:
  - send API requests
  - format responses
  - handle errors gracefully
- Components must NEVER import axios directly.

---

# ==========================
# 6. UI Rules
# ==========================
- Tailwind must be used for styling.
- Components must use semantic HTML.
- Avoid deeply nested DOM structures.
- Use responsive Tailwind classes (`sm:`, `md:`, `lg:`).
- Keep UI consistent and accessible.

---

# ==========================
# 7. Component Communication
# ==========================
- Parent → child: via **props**.
- Child → parent: via **emits**.
- Shared/global state → via **store**.
- Never use global event buses or global variables.

---

# ==========================
# 8. File Organization Rules
# ==========================
- `components/` → reusable UI components.
- `views/` → full-page screens.
- `store/` → global state management.
- `router/` → route definitions.
- `utils/` → helpers (including api.js).
- `assets/` → static resources.

