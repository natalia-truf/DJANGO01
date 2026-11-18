<script setup>
import useShopStore from '@/stores/shopStore';
import { ref, computed, watch } from 'vue';

const shopStore = useShopStore();

const supplierToAdd = ref({});
const supplierToEdit = ref({});

const pagesCount = computed(() => {
  return Math.trunc(shopStore.suppliersTotalCount / shopStore.pageItemsCount) + 1;
});

watch(() => shopStore.suppliersPage, () => {
  shopStore.fetchSuppliers();
});

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