import LoginPage from '@/pages/LoginPage.vue'
import MainPage from '@/pages/MainPage.vue'
import ProductsView from '@/pages/ProductsView.vue'
import CategoriesView from '@/pages/CategoriesView.vue'
import SuppliersView from '@/pages/SuppliersView.vue'
import PointsView from '@/pages/PointsView.vue'
import OrdersView from '@/pages/OrdersView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  linkExactActiveClass: 'active-exact',
  routes: [
    { path: "/", component: MainPage },
    { path: "/login", component: LoginPage },
    { path: "/products", component: ProductsView },
    { path: "/categories", component: CategoriesView },
    { path: "/suppliers", component: SuppliersView },
    { path: "/points", component: PointsView },
    { path: "/orders", component: OrdersView },
  ],
})

export default router