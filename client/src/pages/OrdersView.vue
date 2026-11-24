<script setup>
import useShopStore from '@/stores/shopStore';
import { ref, computed, watch } from 'vue';
import axios from 'axios';

const shopStore = useShopStore();

const orderToAdd = ref({});
const orderToEdit = ref({});

const uniquePoints = computed(() => {
  const seen = new Set();
  return shopStore.allPoints.filter(pt => {
    const name = String(pt.name).toLowerCase().trim();
    if (seen.has(name)) return false;
    seen.add(name);
    return true;
  });
});

const filterProductSearch = ref('');
const filterProductOpen = ref(false);
const filteredFilterProducts = computed(() => {
  const q = filterProductSearch.value.toLowerCase();
  if (!q) return shopStore.allProducts;
  return shopStore.allProducts.filter(p => p.name.toLowerCase().includes(q));
});

function selectFilterProduct(p) {
  shopStore.ordersFilter.product = p.name;
  filterProductSearch.value = p.name;
  filterProductOpen.value = false;
  shopStore.ordersPage = 1;
  shopStore.fetchOrders();
}

function clearFilterProduct() {
  shopStore.ordersFilter.product = '';
  filterProductSearch.value = '';
  filterProductOpen.value = false;
  shopStore.ordersPage = 1;
  shopStore.fetchOrders();
}

const filterPointSearch = ref('');
const filterPointOpen = ref(false);
const filteredFilterPoints = computed(() => {
  const q = filterPointSearch.value.toLowerCase();
  if (!q) return uniquePoints.value;
  return uniquePoints.value.filter(pt => pt.name.toLowerCase().includes(q));
});

function selectFilterPoint(pt) {
  shopStore.ordersFilter.point = pt.name;
  filterPointSearch.value = pt.name;
  filterPointOpen.value = false;
  shopStore.ordersPage = 1;
  shopStore.fetchOrders();
}

function clearFilterPoint() {
  shopStore.ordersFilter.point = '';
  filterPointSearch.value = '';
  filterPointOpen.value = false;
  shopStore.ordersPage = 1;
  shopStore.fetchOrders();
}

const filterOrderId = ref('');
const filterQuantity = ref('');
const filterPriceFrom = ref('');
const filterPriceTo = ref('');

let searchTimeout = null;
function autoApplyFilters() {
  if (searchTimeout) clearTimeout(searchTimeout);
  
  searchTimeout = setTimeout(() => {
    shopStore.ordersFilter.orderId = filterOrderId.value;
    shopStore.ordersFilter.quantity = filterQuantity.value;
    shopStore.ordersFilter.totalPriceFrom = filterPriceFrom.value;
    shopStore.ordersFilter.totalPriceTo = filterPriceTo.value;
    
    shopStore.ordersPage = 1;
    shopStore.fetchOrders();
  }, 500);
}

watch(filterOrderId, autoApplyFilters);
watch(filterQuantity, autoApplyFilters);
watch(filterPriceFrom, autoApplyFilters);
watch(filterPriceTo, autoApplyFilters);

function resetAllFilters() {
  filterOrderId.value = '';
  filterQuantity.value = '';
  filterPriceFrom.value = '';
  filterPriceTo.value = '';
  filterProductSearch.value = '';
  filterPointSearch.value = '';
  
  shopStore.ordersFilter.product = '';
  shopStore.ordersFilter.point = '';
  shopStore.ordersFilter.orderId = '';
  shopStore.ordersFilter.quantity = '';
  shopStore.ordersFilter.totalPriceFrom = '';
  shopStore.ordersFilter.totalPriceTo = '';
  
  shopStore.ordersPage = 1;
  shopStore.fetchOrders();
}

async function exportToExcel() {
  try {
    const response = await axios.get('/api/orders/export-excel/', {
      responseType: 'blob'
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Заказы_${new Date().toISOString().slice(0,10)}.xlsx`);
    
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error("Ошибка при экспорте:", error);
    alert("Не удалось скачать файл.");
  }
}

const pagesCount = computed(() => {
  return Math.trunc(shopStore.ordersTotalCount / shopStore.pageItemsCount) + 1;
});

watch(() => shopStore.ordersPage, () => {
  shopStore.fetchOrders();
});

function onOrderAdd() {
  shopStore.addOrder({ ...orderToAdd.value });
  orderToAdd.value = {};
}

function onRemoveClick(order) {
  shopStore.removeOrder(order.id);
}

function onOrderEditClick(order) {
  orderToEdit.value = {
    ...order,
    product_id: order.product?.id || order.product,
    point_id: order.point?.id || order.point,
  };
}

function onUpdateOrder() {
  shopStore.updateOrder(orderToEdit.value.id, { ...orderToEdit.value });
}
</script>

<template>
  <div class="mt-4">
    <h3 class="mb-4">Заказы</h3>

    <div class="row mb-3">
      <div class="col-md-4">
        <div class="card text-center bg-light">
          <div class="card-body">
            <h5 class="card-title">Всего заказов</h5>
            <p class="card-text fs-4">{{ shopStore.ordersStats.count }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center bg-light">
          <div class="card-body">
            <h5 class="card-title">Продано единиц товара</h5>
            <p class="card-text fs-4">{{ shopStore.ordersStats.total_items }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center bg-light">
          <div class="card-body">
            <h5 class="card-title">Общая сумма</h5>
            <p class="card-text fs-4">{{ shopStore.ordersStats.total_sum }} руб.</p>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent.stop="onOrderAdd" class="mb-4">
      <div class="row g-2 align-items-end">
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="orderToAdd.product_id" required>
              <option :value="p.id" v-for="p in shopStore.products" :key="p.id">{{ p.name }}</option>
            </select>
            <label>Товар</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="orderToAdd.point_id" required>
              <option :value="pt.id" v-for="pt in shopStore.allPoints" :key="pt.id">{{ pt.name }}</option>
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

    <div class="mb-3">
      <button type="button" class="btn btn-success" @click="exportToExcel">
        <i class="bi bi-file-earmark-excel"></i> Скачать Excel
      </button>
    </div>

    <div class="row mb-3 g-2 align-items-end">
      <div class="col-md-3 position-relative">
        <div class="input-group">
          <input type="text" class="form-control" v-model="filterProductSearch" @focus="filterProductOpen = true" @blur="filterProductOpen = false" placeholder="Товар..." autocomplete="off" />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterProduct"><i class="bi bi-x-lg"></i></button>
        </div>
        <div v-if="filterProductOpen && filteredFilterProducts.length" class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" style="max-height: 200px; overflow-y: auto; z-index: 1000;">
          <div v-for="p in filteredFilterProducts" :key="p.id" class="px-3 py-2" style="cursor: pointer;" @mousedown.prevent="selectFilterProduct(p)" :class="{ 'bg-primary text-white': shopStore.ordersFilter.product === p.name }">
            {{ p.name }}
          </div>
        </div>
      </div>

      <div class="col-md-3 position-relative">
        <div class="input-group">
          <input type="text" class="form-control" v-model="filterPointSearch" @focus="filterPointOpen = true" @blur="filterPointOpen = false" placeholder="Точка продажи..." autocomplete="off" />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterPoint"><i class="bi bi-x-lg"></i></button>
        </div>
        <div v-if="filterPointOpen && filteredFilterPoints.length" class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" style="max-height: 200px; overflow-y: auto; z-index: 1000;">
          <div v-for="pt in filteredFilterPoints" :key="pt.id" class="px-3 py-2" style="cursor: pointer;" @mousedown.prevent="selectFilterPoint(pt)" :class="{ 'bg-primary text-white': shopStore.ordersFilter.point === pt.name }">
            {{ pt.name }}
          </div>
        </div>
      </div>

      <div class="col-md-2">
        <input type="text" class="form-control" v-model="filterOrderId" placeholder="№ заказа..." />
      </div>

      <div class="col-md-2">
        <input type="text" class="form-control" v-model="filterQuantity" placeholder="Кол-во..." />
      </div>

      <div class="col-md-1">
        <div class="input-group">
          <span class="input-group-text">От</span>
          <input type="number" class="form-control" v-model="filterPriceFrom" placeholder="0" />
        </div>
      </div>

      <div class="col-md-1">
        <div class="input-group">
          <span class="input-group-text">До</span>
          <input type="number" class="form-control" v-model="filterPriceTo" placeholder="9999" />
        </div>
      </div>
    </div>

    <table class="table align-middle">
      <thead>
        <tr>
          <th>Заказ №</th>
          <th>Товар</th>
          <th>Точка продажи</th>
          <th class="text-end">Кол-во</th>
          <th class="text-end">Сумма</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in shopStore.orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.product?.name || 'Удален' }}</td>
          <td>{{ order.point?.name || 'Удалена' }}</td>
          <td class="text-end">{{ order.quantity }}</td>
          <td class="text-end">{{ order.total_price }} руб.</td>
          <td class="text-center">
            <div class="d-flex gap-2 justify-content-center">
              <button class="btn btn-success btn-sm" @click="onOrderEditClick(order)" data-bs-toggle="modal" data-bs-target="#editOrderModal"><i class="bi bi-pen-fill"></i></button>
              <button class="btn btn-danger btn-sm" @click="onRemoveClick(order)"><i class="bi bi-x"></i></button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <nav aria-label="Page navigation" v-if="shopStore.ordersTotalCount > 10">
      <ul class="pagination justify-content-center">
        <li class="page-item" @click="shopStore.ordersPage -= 1" :class="{ disabled: shopStore.ordersPage === 1 }"><a class="page-link" href="#">Previous</a></li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage - 1" class="page-item" v-if="shopStore.ordersPage - 1 > 0"><a class="page-link">{{ shopStore.ordersPage - 1 }}</a></li>
        <li class="page-item active" v-if="shopStore.ordersPage > 0"><span class="page-link">{{ shopStore.ordersPage }}</span></li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage + 1" class="page-item" v-if="shopStore.ordersPage + 1 < pagesCount"><a class="page-link">{{ shopStore.ordersPage + 1 }}</a></li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage + 2" class="page-item" v-if="shopStore.ordersPage + 2 < pagesCount"><a class="page-link">{{ shopStore.ordersPage + 2 }}</a></li>
        <li class="page-item" @click="shopStore.ordersPage += 1" :class="{ disabled: shopStore.ordersPage === pagesCount }"><a class="page-link" href="#">Next</a></li>
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
                <option :value="p.id" v-for="p in shopStore.products" :key="p.id">{{ p.name }}</option>
              </select>
              <label>Товар</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" v-model="orderToEdit.point_id">
                <option :value="pt.id" v-for="pt in uniquePoints" :key="pt.id">{{ pt.name }}</option>
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