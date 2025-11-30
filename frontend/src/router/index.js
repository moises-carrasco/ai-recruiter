/**
 * Vue Router configuration
 */

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/candidates',
      name: 'candidates',
      component: () => import('../views/CandidatesView.vue')
    },
    {
      path: '/interviews',
      name: 'interviews',
      component: () => import('../views/InterviewsView.vue')
    },
    {
      path: '/interviews/:id',
      name: 'interview-detail',
      component: () => import('../views/InterviewDetailView.vue')
    },
    {
      path: '/interview/:link',
      name: 'interview-execution',
      component: () => import('../views/InterviewExecutionView.vue')
    }
  ]
})

// TODO: Add navigation guards for authentication
// router.beforeEach((to, from, next) => {
//   // Authentication logic
// })

export default router
