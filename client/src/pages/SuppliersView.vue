<script setup>
import useShopStore from '@/stores/shopStore';
import useProfileStore from '@/stores/profileStore';
import { ref, computed, watch } from 'vue';

const shopStore = useShopStore();
const profileStore = useProfileStore();

const supplierToAdd = ref({});
const supplierToEdit = ref({});

const pagesCount = computed(() => {
  return Math.trunc(shopStore.suppliersTotalCount / shopStore.pageItemsCount) + 1;
});

watch(() => shopStore.suppliersPage, () => {
  shopStore.fetchSuppliers();
});

const nameFilterSearch = ref('');
const nameFilterOpen = ref(false);
const filteredSuppliersByName = computed(() => {
  const q = nameFilterSearch.value.toLowerCase();
  if (!q) return shopStore.allSuppliers;
  return shopStore.allSuppliers.filter(s => s.name.toLowerCase().includes(q));
});
function selectFilterName(s) {
  shopStore.suppliersFilter.name = s.name;
  nameFilterSearch.value = s.name;
  nameFilterOpen.value = false;
  shopStore.suppliersPage = 1;
  shopStore.fetchSuppliers();
}
function clearFilterName() {
  shopStore.suppliersFilter.name = '';
  nameFilterSearch.value = '';
  nameFilterOpen.value = false;
  shopStore.suppliersPage = 1;
  shopStore.fetchSuppliers();
}

const phoneFilterSearch = ref('');
const phoneFilterOpen = ref(false);
const filteredSuppliersByPhone = computed(() => {
  const q = phoneFilterSearch.value.trim();
  if (!q) return shopStore.allSuppliers;
  return shopStore.allSuppliers.filter(s => String(s.phone).includes(q));
});
function selectFilterPhone(s) {
  shopStore.suppliersFilter.phone = s.phone;
  phoneFilterSearch.value = s.phone;
  phoneFilterOpen.value = false;
  shopStore.suppliersPage = 1;
  shopStore.fetchSuppliers();
}
function clearFilterPhone() {
  shopStore.suppliersFilter.phone = '';
  phoneFilterSearch.value = '';
  phoneFilterOpen.value = false;
  shopStore.suppliersPage = 1;
  shopStore.fetchSuppliers();
}

function onSupplierAdd() {
  shopStore.addSupplier({ ...supplierToAdd.value });
  supplierToAdd.value = {};
}

function onRemoveClick(supplier) {
  shopStore.removeSupplier(supplier.id);
}

function onSupplierEditClick(supplier) {
  supplierToEdit.value = { ...supplier };
}

function onUpdateSupplier() {
  shopStore.updateSupplier(supplierToEdit.value.id, { ...supplierToEdit.value });
}
</script>

<template>
  <div class="mt-4">
    <h3 class="mb-4">Поставщики</h3>

    <div class="row mb-3" v-if="profileStore.isSuperuser || profileStore.userRole === 'seller'">
      <div class="col-md-12">
        <div class="card text-center bg-light">
          <div class="card-body">
            <h5 class="card-title">Всего поставщиков</h5>
            <p class="card-text fs-4">{{ shopStore.suppliersStats.count }}</p>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent.stop="onSupplierAdd" class="mb-4">
      <div class="row g-2">
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="supplierToAdd.name" required />
          <label>Название</label>
        </div></div>
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="supplierToAdd.phone" required />
          <label>Телефон</label>
        </div></div>
        <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
      </div>
    </form>

    <div class="row mb-3">
      <div class="col-md-6 position-relative">
        <div class="input-group">
          <input type="text" class="form-control" v-model="nameFilterSearch" @focus="nameFilterOpen = true" @blur="nameFilterOpen = false" placeholder="Фильтр по названию..." autocomplete="off" />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterName"><i class="bi bi-x-lg"></i></button>
        </div>
        <div v-if="nameFilterOpen && filteredSuppliersByName.length" class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" style="max-height: 200px; overflow-y: auto; z-index: 1000;">
          <div v-for="s in filteredSuppliersByName" :key="s.id" class="px-3 py-2" style="cursor: pointer;" @mousedown.prevent="selectFilterName(s)" :class="{ 'bg-primary text-white': shopStore.suppliersFilter.name === s.name }">
            {{ s.name }}
          </div>
        </div>
      </div>

      <div class="col-md-6 position-relative">
        <div class="input-group">
          <input type="text" class="form-control" v-model="phoneFilterSearch" @focus="phoneFilterOpen = true" @blur="phoneFilterOpen = false" placeholder="Фильтр по телефону..." autocomplete="off" />
          <button class="btn btn-outline-secondary" type="button" @click="clearFilterPhone"><i class="bi bi-x-lg"></i></button>
        </div>
        <div v-if="phoneFilterOpen && filteredSuppliersByPhone.length" class="position-absolute w-100 bg-white border rounded shadow-sm mt-1" style="max-height: 200px; overflow-y: auto; z-index: 1000;">
          <div v-for="s in filteredSuppliersByPhone" :key="s.id" class="px-3 py-2" style="cursor: pointer;" @mousedown.prevent="selectFilterPhone(s)" :class="{ 'bg-primary text-white': shopStore.suppliersFilter.phone === s.phone }">
            {{ s.phone }}
          </div>
        </div>
      </div>
    </div>

    <table class="table align-middle">
      <thead>
        <tr>
          <th>Название</th>
          <th>Телефон</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in shopStore.suppliers" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.phone }}</td>
          <td class="text-center">
            <div class="d-flex gap-2 justify-content-center">
              <button class="btn btn-success btn-sm" @click="onSupplierEditClick(item)" data-bs-toggle="modal" data-bs-target="#editSupplierModal">
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

    <nav aria-label="Page navigation" v-if="shopStore.suppliersTotalCount > 10">
      <ul class="pagination justify-content-center">
        <li class="page-item" @click="shopStore.suppliersPage -= 1" :class="{ disabled: shopStore.suppliersPage === 1 }">
          <a class="page-link" href="#">Previous</a>
        </li>
        <li @click="shopStore.suppliersPage = shopStore.suppliersPage - 1" class="page-item" v-if="shopStore.suppliersPage - 1 > 0">
          <a class="page-link">{{ shopStore.suppliersPage - 1 }}</a>
        </li>
        <li class="page-item active" v-if="shopStore.suppliersPage > 0">
          <span class="page-link">{{ shopStore.suppliersPage }}</span>
        </li>
        <li @click="shopStore.suppliersPage = shopStore.suppliersPage + 1" class="page-item" v-if="shopStore.suppliersPage + 1 < pagesCount">
          <a class="page-link">{{ shopStore.suppliersPage + 1 }}</a>
        </li>
        <li @click="shopStore.suppliersPage = shopStore.suppliersPage + 2" class="page-item" v-if="shopStore.suppliersPage + 2 < pagesCount">
          <a class="page-link">{{ shopStore.suppliersPage + 2 }}</a>
        </li>
        <li class="page-item" @click="shopStore.suppliersPage += 1" :class="{ disabled: shopStore.suppliersPage === pagesCount }">
          <a class="page-link" href="#">Next</a>
        </li>
      </ul>
    </nav>

    <div class="modal fade" id="editSupplierModal" tabindex="-1">
      <div class="modal-dialog"><div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="supplierToEdit.name" /><label>Название</label>
          </div>
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="supplierToEdit.phone" /><label>Телефон</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateSupplier">Сохранить</button>
        </div>
      </div></div>
    </div>
  </div>
</template>