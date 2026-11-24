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

const uniquePointsByName = computed(() => {
  const seen = new Set();
  return shopStore.allPoints.filter(p => {
    const name = String(p.name).toLowerCase().trim();
    if (seen.has(name)) return false;
    seen.add(name);
    return true;
  });
});

const uniquePointsByAddress = computed(() => {
  const seen = new Set();
  return shopStore.allPoints.filter(p => {
    const address = String(p.address).toLowerCase().trim();
    if (seen.has(address)) return false;
    seen.add(address);
    return true;
  });
});

const nameFilterSearch = ref('');
const nameFilterOpen = ref(false);

const filteredPointsByName = computed(() => {
  const q = nameFilterSearch.value.toLowerCase();
  if (!q) return uniquePointsByName.value;
  return uniquePointsByName.value.filter(p => p.name.toLowerCase().includes(q));
});

function selectFilterName(p) {
  shopStore.pointsFilter.name = p.name;
  nameFilterSearch.value = p.name;
  nameFilterOpen.value = false;
  shopStore.pointsPage = 1;
  shopStore.fetchPoints();
}

function clearFilterName() {
  shopStore.pointsFilter.name = '';
  nameFilterSearch.value = '';
  nameFilterOpen.value = false;
  shopStore.pointsPage = 1;
  shopStore.fetchPoints();
}

const addressFilterSearch = ref('');
const addressFilterOpen = ref(false);

const filteredPointsByAddress = computed(() => {
  const q = addressFilterSearch.value.toLowerCase();
  if (!q) return uniquePointsByAddress.value;
  return uniquePointsByAddress.value.filter(p => p.address.toLowerCase().includes(q));
});

function selectFilterAddress(p) {
  shopStore.pointsFilter.address = p.address;
  addressFilterSearch.value = p.address;
  addressFilterOpen.value = false;
  shopStore.pointsPage = 1;
  shopStore.fetchPoints();
}

function clearFilterAddress() {
  shopStore.pointsFilter.address = '';
  addressFilterSearch.value = '';
  addressFilterOpen.value = false;
  shopStore.pointsPage = 1;
  shopStore.fetchPoints();
}

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
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="pointToAdd.name" required />
            <label>Название</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="pointToAdd.address" required />
            <label>Адрес</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div class="row mb-3">
      <div class="col-md-6 position-relative">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            v-model="nameFilterSearch" 
            @focus="nameFilterOpen = true" 
            @blur="nameFilterOpen = false" 
            placeholder="Фильтр по названию..." 
            autocomplete="off" 
          />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterName">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div 
          v-if="nameFilterOpen && filteredPointsByName.length" 
          class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" 
          style="max-height: 200px; overflow-y: auto; z-index: 1000;"
        >
          <div 
            v-for="p in filteredPointsByName" 
            :key="p.id" 
            class="px-3 py-2" 
            style="cursor: pointer;" 
            @mousedown.prevent="selectFilterName(p)" 
            :class="{ 'bg-primary text-white': shopStore.pointsFilter.name === p.name }"
          >
            {{ p.name }}
          </div>
        </div>
      </div>

      <div class="col-md-6 position-relative">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            v-model="addressFilterSearch" 
            @focus="addressFilterOpen = true" 
            @blur="addressFilterOpen = false" 
            placeholder="Фильтр по адресу..." 
            autocomplete="off" 
          />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterAddress">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div 
          v-if="addressFilterOpen && filteredPointsByAddress.length" 
          class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" 
          style="max-height: 200px; overflow-y: auto; z-index: 1000;"
        >
          <div 
            v-for="p in filteredPointsByAddress" 
            :key="p.id" 
            class="px-3 py-2" 
            style="cursor: pointer;" 
            @mousedown.prevent="selectFilterAddress(p)" 
            :class="{ 'bg-primary text-white': shopStore.pointsFilter.address === p.address }"
          >
            {{ p.address }}
          </div>
        </div>
      </div>
    </div>

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
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="pointToEdit.name" />
              <label>Название</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="pointToEdit.address" />
              <label>Адрес</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdatePoint">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>