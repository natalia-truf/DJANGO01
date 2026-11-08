<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue'
import axios from 'axios'

const suppliers = ref([])
const supplierToAdd = ref({})
const supplierToEdit = ref({})

const page = ref(1)
const pageItemsCount = ref(10)
const totalCount = ref(0)
const loading = ref(false)

async function fetchSuppliers() {
  loading.value = true
  const r = await axios.get('/api/suppliers/', { params: { page: page.value } })
  suppliers.value = r.data.results || r.data
  totalCount.value = r.data.count || 0
  loading.value = false
}

const pagesCount = computed(() => {
  return Math.trunc(totalCount.value / pageItemsCount.value) + 1
})

watch(page, () => {
  fetchSuppliers()
})

function prevPage() {
  if (page.value > 1) page.value -= 1
}

function nextPage() {
  if (page.value < pagesCount.value) page.value += 1
}

async function onSupplierAdd() {
  await axios.post('/api/suppliers/', { ...supplierToAdd.value })
  await fetchSuppliers()
  supplierToAdd.value = {}
}

async function onRemoveClick(supplier) {
  await axios.delete(`/api/suppliers/${supplier.id}/`)
  await fetchSuppliers()
}

function onSupplierEditClick(supplier) {
  supplierToEdit.value = { ...supplier }
}

async function onUpdateSupplier() {
  await axios.put(`/api/suppliers/${supplierToEdit.value.id}/`, { ...supplierToEdit.value })
  await fetchSuppliers()
}

onBeforeMount(fetchSuppliers)
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

    <div v-if="loading" class="text-center my-3">Гружу данные...</div>

    <table class="table align-middle" v-else>
      <thead>
        <tr>
          <th>Название</th>
          <th>Телефон</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in suppliers" :key="item.id">
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