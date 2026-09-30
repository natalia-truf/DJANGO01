<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const orders = ref([])
const products = ref([])
const points = ref([])
const orderToAdd = ref({})
const orderToEdit = ref({})

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function fetchPoints() {
  const r = await axios.get('/api/points/')
  points.value = r.data
}

async function onOrderAdd() {
  await axios.post('/api/orders/', { ...orderToAdd.value })
  await fetchOrders()
}

async function onRemoveClick(order) {
  await axios.delete(`/api/orders/${order.id}/`)
  await fetchOrders()
}

function onOrderEditClick(order) {
  orderToEdit.value = {
    ...order,
    product_id: order.product?.id ?? order.product,
    point_id: order.point?.id ?? order.point,
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
  <div class=" mt-4">
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

    <div v-for="item in orders" :key="item.id" class="border rounded p-3 mb-2">
      <div class="row align-items-center">
        <div class="col-2">Заказ #{{ item.id }}</div>
        <div class="col-3">{{ item.product?.name }}</div>
        <div class="col-2 text-end">{{ item.quantity }} шт.</div>
        <div class="col-3">{{ item.point?.name }}</div>

        <div class="col-2 d-flex gap-3 justify-content-center">
          <button class="btn btn-success"
                  @click="onOrderEditClick(item)"
                  data-bs-toggle="modal"
                  data-bs-target="#editOrderModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Модалка редактирования -->
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
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="orderToEdit.quantity" />
              <label>Количество</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateOrder">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>