<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const points = ref([])
const pointToAdd = ref({})
const pointToEdit = ref({})

async function fetchPoints() {
  const r = await axios.get('/api/points/')
  points.value = r.data
}

async function onPointAdd() {
  await axios.post('/api/points/', { ...pointToAdd.value })
  await fetchPoints()
}

async function onRemoveClick(point) {
  await axios.delete(`/api/points/${point.id}/`)
  await fetchPoints()
}

function onPointEditClick(point) {
  pointToEdit.value = { ...point }
}

async function onUpdatePoint() {
  await axios.put(`/api/points/${pointToEdit.value.id}/`, { ...pointToEdit.value })
  await fetchPoints()
}

onBeforeMount(fetchPoints)
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-4">Точки продажи</h3>

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

    <div v-for="item in points" :key="item.id" class="border rounded p-3 mb-2">
      <div class="row align-items-center">
        <div class="col-5">{{ item.name }}</div>
        <div class="col-4">{{ item.address }}</div>

        <div class="col-3 d-flex gap-3 justify-content-center">
          <button class="btn btn-success"
                  @click="onPointEditClick(item)"
                  data-bs-toggle="modal"
                  data-bs-target="#editPointModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Модалка редактирования -->
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
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdatePoint">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>