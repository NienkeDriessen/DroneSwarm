import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CharadesView from '../views/CharadesView.vue'
import DrawPathView from '../views/DrawPathsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/charades',
      name: 'charades',
      component: CharadesView,
    },
    {
      path: '/draw-your-own-path',
      name: 'draw-path',
      component: DrawPathView,
    },
  ],
})

export default router
