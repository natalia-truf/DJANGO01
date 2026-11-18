<script setup>
import useShopStore from '@/stores/shopStore';
import useProfileStore from '@/stores/profileStore';
import { ref, computed, watch } from 'vue';

const shopStore = useShopStore();
const profileStore = useProfileStore();

const orderToAdd = ref({});
const orderToEdit = ref({});

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
      <div class="row g-2">
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
              <option :value="pt.id" v-for="pt in shopStore.points" :key="pt.id">{{ pt.name }}</option>
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
          <td class="text-end">{{ order.total_price }} руб.</td> <!-- ВЫВОДИМ СУММУ -->
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

    <nav aria-label="Page navigation" v-if="shopStore.ordersTotalCount > 10">
      <ul class="pagination justify-content-center">
        <li class="page-item" @click="shopStore.ordersPage -= 1" :class="{ disabled: shopStore.ordersPage === 1 }">
          <a class="page-link" href="#">Previous</a>
        </li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage - 1" class="page-item" v-if="shopStore.ordersPage - 1 > 0">
          <a class="page-link">{{ shopStore.ordersPage - 1 }}</a>
        </li>
        <li class="page-item active" v-if="shopStore.ordersPage > 0">
          <span class="page-link">{{ shopStore.ordersPage }}</span>
        </li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage + 1" class="page-item" v-if="shopStore.ordersPage + 1 < pagesCount">
          <a class="page-link">{{ shopStore.ordersPage + 1 }}</a>
        </li>
        <li @click="shopStore.ordersPage = shopStore.ordersPage + 2" class="page-item" v-if="shopStore.ordersPage + 2 < pagesCount">
          <a class="page-link">{{ shopStore.ordersPage + 2 }}</a>
        </li>
        <li class="page-item" @click="shopStore.ordersPage += 1" :class="{ disabled: shopStore.ordersPage === pagesCount }">
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
                <option :value="p.id" v-for="p in shopStore.products" :key="p.id">{{ p.name }}</option>
              </select>
              <label>Товар</label>
            </div>
            <div class="form-floating mb-2">
              <select class="form-select" v-model="orderToEdit.point_id">
                <option :value="pt.id" v-for="pt in shopStore.points" :key="pt.id">{{ pt.name }}</option>
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