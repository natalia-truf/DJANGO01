import { createRouter, createWebHistory } from 'vue-router'
import Categories from '@/components/Categories.vue'
import Suppliers from '@/components/Suppliers.vue'
import Points from '@/components/Points.vue'
import Products from '@/components/Products.vue'
import Orders from '@/components/Orders.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/categories', component: Categories },
    { path: '/suppliers', component: Suppliers },
    { path: '/points', component: Points },
    { path: '/products', component: Products },
    { path: '/orders', component: Orders },
  ]
})

export default router