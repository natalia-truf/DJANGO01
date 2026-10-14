<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const suppliers = ref([])
const supplierToAdd = ref({})
const supplierToEdit = ref({})

async function fetchSuppliers() {
  const r = await axios.get('/api/suppliers/')
  suppliers.value = r.data
}

async function onSupplierAdd() {
  await axios.post('/api/suppliers/', { ...supplierToAdd.value })
  await fetchSuppliers()
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
  <div class=" mt-4">
    <h3 class="mb-4">Поставщики</h3>

    <form @submit.prevent.stop="onSupplierAdd" class="mb-4">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="supplierToAdd.name" required />
            <label>Название</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="supplierToAdd.phone" required />
            <label>Телефон</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in suppliers" :key="item.id" class="border rounded p-3 mb-2">
      <div class="row align-items-center">
        <div class="col-5">{{ item.name }}</div>
        <div class="col-4">{{ item.phone }}</div>

        <div class="col-3 d-flex gap-3 justify-content-center">
          <button class="btn btn-success"
                  @click="onSupplierEditClick(item)"
                  data-bs-toggle="modal"
                  data-bs-target="#editSupplierModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Модалка редактирования -->
    <div class="modal fade" id="editSupplierModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="supplierToEdit.name" />
              <label>Название</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="supplierToEdit.phone" />
              <label>Телефон</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateSupplier">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>