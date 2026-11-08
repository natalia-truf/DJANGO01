<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue'
import axios from 'axios'

const orders = ref([])
const products = ref([])
const points = ref([])
const orderToAdd = ref({})
const orderToEdit = ref({})

const page = ref(1)
const pageItemsCount = ref(10)
const totalCount = ref(0)
const loading = ref(false)

async function fetchOrders() {
  loading.value = true
  const r = await axios.get('/api/orders/', { params: { page: page.value } })
  orders.value = r.data.results || r.data
  totalCount.value = r.data.count || 0
  loading.value = false
}

async function fetchProducts() {
  const r = await axios.get('/api/products/', { params: { page_size: 10000 } })
  products.value = r.data.results || r.data
}

async function fetchPoints() {
  const r = await axios.get('/api/points/', { params: { page_size: 10000 } })
  points.value = r.data.results || r.data
}

const pagesCount = computed(() => {
  return Math.trunc(totalCount.value / pageItemsCount.value) + 1
})

watch(page, () => {
  fetchOrders()
})

function prevPage() {
  if (page.value > 1) page.value -= 1
}

function nextPage() {
  if (page.value < pagesCount.value) page.value += 1
}

async function onOrderAdd() {
  await axios.post('/api/orders/', { ...orderToAdd.value })
  await fetchOrders()
  orderToAdd.value = {}
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`)
  await fetchOrders()
}

function onOrderEditClick(order) {
  orderToEdit.value = {
    ...order,
    product_id: order.product?.id || order.product,
    point_id: order.point?.id || order.point,
  }
}

async function onUpdateOrder() {
  await axios.put(`/api/orders/${orderToEdit.value.id}/`, { ...orderToEdit.value })
  await fetchOrders()
}

onBeforeMount(() => {
  fetchOrders()
  fetchProducts()
  fetchPoints()
})
</script>

<template>
  <div class="mt-4">
    <h3 class="mb-4">Заказы</h3>

    <form @submit.prevent.stop="onOrderAdd" class="mb-4">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="orderToAdd.product_id" required>
              <option :value="p.id" v-for="p in products" :key="p.id">{{ p.name }}</option>
            </select>
            <label>Товар</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="orderToAdd.point_id" required>
              <option :value="pt.id" v-for="pt in points" :key="pt.id">{{ pt.name }}</option>
            </select>
            <label>Точка продажи</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="orderToAdd.quantity" required />
            <label>Количество</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-if="loading" class="text-center my-3">Гружу данные...</div>

    <table class="table align-middle" v-else>
      <thead>
        <tr>
          <th>Заказ №</th>
          <th>Товар</th>
          <th>Точка продажи</th>
          <th class="text-end">Кол-во</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.product?.name || 'Удален' }}</td>
          <td>{{ order.point?.name || 'Удалена' }}</td>
          <td class="text-end">{{ order.quantity }}</td>
          <td class="text-center">
            <div class="d-flex gap-2 justify-content-center">
              <button class="btn btn-success btn-sm" @click="onOrderEditClick(order)" data-bs-toggle="modal" data-bs-target="#editOrderModal">
                <i class="bi bi-pen-fill"></i>
              </button>
              <button class="btn btn-danger btn-sm" @click="onRemoveClick(order)">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <nav aria-label="Page navigation" v-if="!loading && totalCount > 10">
      <ul class="pagination justify-content-center">
        <li class="page-item" @click="prevPage" :class="{ disabled: page === 1 }">
          <a class="page-link" href="#">Previous</a>
        </li>
        <li @click="prevPage" class="page-item" v-if="page - 1 > 0">
          <a class="page-link">{{ page - 1 }}</a>
        </li>
        <li class="page-item active" v-if="page > 0">
          <span class="page-link">{{ page }}</span>
        </li>
        <li @click="page = page + 1" class="page-item" v-if="page + 1 < pagesCount">
          <a class="page-link">{{ page + 1 }}</a>
        </li>
        <li @click="page = page + 2" class="page-item" v-if="page + 2 < pagesCount">
          <a class="page-link">{{ page + 2 }}</a>
        </li>
        <li class="page-item" @click="nextPage" :class="{ disabled: page === pagesCount }">
          <a class="page-link" href="#">Next</a>
        </li>
      </ul>
    </nav>

    <div class="modal fade" id="editOrderModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <select class="form-select" v-model="orderToEdit.product_id">
                <option :value="p.id" v-for="p in products" :key="p.id">{{ p.name }}</option>
              </select>
              <label>Товар</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" v-model="orderToEdit.point_id">
                <option :value="pt.id" v-for="pt in points" :key="pt.id">{{ pt.name }}</option>
              </select>
              <label>Точка продажи</label>
            </div>
            <div class="form-floating">
              <input type="number" class="form-control" v-model="orderToEdit.quantity" />
              <label>Количество</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateOrder">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>