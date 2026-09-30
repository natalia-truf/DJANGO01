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
  <div>
    <h3>Поставщики</h3>

    <form @submit.prevent.stop="onSupplierAdd">
      <input type="text" v-model="supplierToAdd.name" placeholder="Название" required />
      <input type="text" v-model="supplierToAdd.phone" placeholder="Телефон" required />
      <button>Добавить</button>
    </form>

    <div v-for="item in suppliers" :key="item.id" class="item">
      <div>{{ item.name }} — {{ item.phone }}</div>
      <button @click="onSupplierEditClick(item)" data-bs-toggle="modal" data-bs-target="#editSupplierModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
    </div>

    <div class="modal fade" id="editSupplierModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" v-model="supplierToEdit.name" placeholder="Название" />
            <input type="text" v-model="supplierToEdit.phone" placeholder="Телефон" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateSupplier">
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