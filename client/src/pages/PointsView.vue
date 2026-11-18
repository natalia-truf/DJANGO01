<script setup>
import useShopStore from '@/stores/shopStore';
import useProfileStore from '@/stores/profileStore';
import { ref, computed, watch } from 'vue';

const shopStore = useShopStore();
const profileStore = useProfileStore();

const pointToAdd = ref({});
const pointToEdit = ref({});

const pagesCount = computed(() => {
  return Math.trunc(shopStore.pointsTotalCount / shopStore.pageItemsCount) + 1;
});

watch(() => shopStore.pointsPage, () => {
  shopStore.fetchPoints();
});

function onPointAdd() {
  shopStore.addPoint({ ...pointToAdd.value });
  pointToAdd.value = {};
}

function onRemoveClick(point) {
  shopStore.removePoint(point.id);
}

function onPointEditClick(point) {
  pointToEdit.value = { ...point };
}

function onUpdatePoint() {
  shopStore.updatePoint(pointToEdit.value.id, { ...pointToEdit.value });
}
</script>

<template>
  <div class="mt-4">
    <h3 class="mb-4">Точки продажи</h3>

    <div class="row mb-3" v-if="profileStore.isSuperuser || profileStore.userRole === 'seller'">
      <div class="col-md-12">
        <div class="card text-center bg-light">
          <div class="card-body">
            <h5 class="card-title">Всего точек продажи</h5>
            <p class="card-text fs-4">{{ shopStore.pointsStats.count }}</p>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent.stop="onPointAdd" class="mb-4">
      <div class="row g-2">
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="pointToAdd.name" required />
          <label>Название</label>
        </div></div>
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="pointToAdd.address" required />
          <label>Адрес</label>
        </div></div>
        <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
      </div>
    </form>

    <table class="table align-middle">
      <thead>
        <tr>
          <th>Название</th>
          <th>Адрес</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in shopStore.points" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.address }}</td>
          <td class="text-center">
            <div class="d-flex gap-2 justify-content-center">
              <button class="btn btn-success btn-sm" @click="onPointEditClick(item)" data-bs-toggle="modal" data-bs-target="#editPointModal">
                <i class="bi bi-pen-fill"></i>
              </button>
              <button class="btn btn-danger btn-sm" @click="onRemoveClick(item)">
                <i class="bi bi-x"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <nav aria-label="Page navigation" v-if="shopStore.pointsTotalCount > 10">
      <ul class="pagination justify-content-center">
        <li class="page-item" @click="shopStore.pointsPage -= 1" :class="{ disabled: shopStore.pointsPage === 1 }">
          <a class="page-link" href="#">Previous</a>
        </li>
        <li @click="shopStore.pointsPage = shopStore.pointsPage - 1" class="page-item" v-if="shopStore.pointsPage - 1 > 0">
          <a class="page-link">{{ shopStore.pointsPage - 1 }}</a>
        </li>
        <li class="page-item active" v-if="shopStore.pointsPage > 0">
          <span class="page-link">{{ shopStore.pointsPage }}</span>
        </li>
        <li @click="shopStore.pointsPage = shopStore.pointsPage + 1" class="page-item" v-if="shopStore.pointsPage + 1 < pagesCount">
          <a class="page-link">{{ shopStore.pointsPage + 1 }}</a>
        </li>
        <li @click="shopStore.pointsPage = shopStore.pointsPage + 2" class="page-item" v-if="shopStore.pointsPage + 2 < pagesCount">
          <a class="page-link">{{ shopStore.pointsPage + 2 }}</a>
        </li>
        <li class="page-item" @click="shopStore.pointsPage += 1" :class="{ disabled: shopStore.pointsPage === pagesCount }">
          <a class="page-link" href="#">Next</a>
        </li>
      </ul>
    </nav>

    <div class="modal fade" id="editPointModal" tabindex="-1">
      <div class="modal-dialog"><div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="pointToEdit.name" /><label>Название</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="pointToEdit.address" /><label>Адрес</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdatePoint">Сохранить</button>
        </div>
      </div></div>
    </div>
  </div>
</template>