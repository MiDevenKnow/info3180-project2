import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: 'home', component: () => import('../components/Home.vue')},

    { path: "/register", name: 'register', component: () => import('../components/RegisterForm.vue')},

    { path: "/login", name: 'login', component: () => import('../components/LoginForm.vue')},

    { path: "/logout", name: 'logout', component: () => import('../components/Logout.vue')},

    { path: "/explore", name: 'explore', component: () => import('../components/Explore.vue')},

    { path: "/users/:user_id", name:'profile', component: () => import('../components/Profile.vue')},
    
    { path: "/cars/new", component: () => import('../components/CarForm.vue')},

    { path: "/cars/:car_id", name:'carDetails', component: () => import('../components/CarDetails.vue')},
  ]
})

export default router
