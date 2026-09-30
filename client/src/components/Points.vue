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
  <div>
    <h3>Точки продажи</h3>

    <form @submit.prevent.stop="onPointAdd">
      <input type="text" v-model="pointToAdd.name" placeholder="Название" required />
      <input type="text" v-model="pointToAdd.address" placeholder="Адрес" required />
      <button>Добавить</button>
    </form>

    <div v-for="item in points" :key="item.id" class="item">
      <div>{{ item.name }} — {{ item.address }}</div>
      <button @click="onPointEditClick(item)" data-bs-toggle="modal" data-bs-target="#editPointModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
    </div>

    <div class="modal fade" id="editPointModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" v-model="pointToEdit.name" placeholder="Название" />
            <input type="text" v-model="pointToEdit.address" placeholder="Адрес" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdatePoint">
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