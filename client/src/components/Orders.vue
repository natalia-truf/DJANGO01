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
  orderToEdit.value = { ...order }
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
  <div>
    <h3>Заказы</h3>

    <form @submit.prevent.stop="onOrderAdd">
      <select v-model="orderToAdd.product_id" required>
        <option :value="p.id" v-for="p in products" :key="p.id">{{ p.name }}</option>
      </select>
      <select v-model="orderToAdd.point_id" required>
        <option :value="pt.id" v-for="pt in points" :key="pt.id">{{ pt.name }}</option>
      </select>
      <input type="number" v-model="orderToAdd.quantity" placeholder="Количество" required />
      <button>Добавить</button>
    </form>

    <div v-for="item in orders" :key="item.id" class="item">
      <div>Заказ #{{ item.id }} — {{ item.product?.name }} — {{ item.quantity }} шт. — {{ item.point?.name }}</div>
      <button @click="onOrderEditClick(item)" data-bs-toggle="modal" data-bs-target="#editOrderModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
    </div>

    <div class="modal fade" id="editOrderModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <select v-model="orderToEdit.product_id">
              <option :value="p.id" v-for="p in products" :key="p.id">{{ p.name }}</option>
            </select>
            <select v-model="orderToEdit.point_id">
              <option :value="pt.id" v-for="pt in points" :key="pt.id">{{ pt.name }}</option>
            </select>
            <input type="number" v-model="orderToEdit.quantity" placeholder="Количество" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateOrder">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item { margin-bottom: 5px; }
</style>