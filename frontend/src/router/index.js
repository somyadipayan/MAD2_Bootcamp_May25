import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import CreateSection from '@/views/CreateSection.vue'
import AllSections from '@/views/AllSections.vue'
import EditSection from '@/views/EditSection.vue'
import AddBook from '@/views/AddBook.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/sections',
    component: AllSections,
  },
  {
    path: '/create-section',
    component: CreateSection,
    meta: { requiresLibrarian: true }
  },
  {
    path: '/edit-section/:id',
    component: EditSection
  },
  {
    path: '/addbook/:id',
    name: 'addbook',
    component: AddBook
  }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

import { getUserInfo } from '@/utils/auth'

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresLibrarian) {
    const user = await getUserInfo();
    if (user && user.librarian) {
      next();
    } else {
      alert('You must be a librarian to access this page');
      next('/login');
    }
  } else {
    next();
  }
});

export default router
