import { createRouter, createWebHistory } from 'vue-router'
import CategoriesView from '@/views/CategoriesView.vue'
import SuppliersView from '@/views/SuppliersView.vue'
import PointsView from '@/views/PointsView.vue'
import ProductsView from '@/views/ProductsView.vue'
import OrdersView from '@/views/OrdersView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/products', component: ProductsView },
    { path: '/categories', component: CategoriesView },
    { path: '/suppliers', component: SuppliersView },
    { path: '/points', component: PointsView },
    { path: '/orders', component: OrdersView },
  ]
})

export default router