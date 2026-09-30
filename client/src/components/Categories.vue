<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const categories = ref([])
const categoryToAdd = ref({})
const categoryToEdit = ref({})
const categoriesPictureRef = ref()
const categoryAddImageUrl = ref()
const categoryEditPictureRef = ref()
const categoryEditImageUrl = ref()

// Для просмотра картинки
const viewImageUrl = ref()

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

function categoriesAddPictureChange() {
  categoryAddImageUrl.value = URL.createObjectURL(categoriesPictureRef.value.files[0])
}

function categoriesEditPictureChange() {
  categoryEditImageUrl.value = URL.createObjectURL(categoryEditPictureRef.value.files[0])
}

// Открытие картинки для просмотра
function onImageClick(category) {
  viewImageUrl.value = category.picture
}

async function onCategoryAdd() {
  const formData = new FormData()
  if (categoriesPictureRef.value?.files[0]) {
    formData.append('picture', categoriesPictureRef.value.files[0])
  }
  formData.set('name', categoryToAdd.value.name)

  await axios.post("/api/categories/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchCategories()
}

async function onRemoveClick(category) {
  await axios.delete(`/api/categories/${category.id}/`)
  await fetchCategories()
}

function onCategoryEditClick(category) {
  categoryToEdit.value = { ...category }
  categoryEditImageUrl.value = category.picture
}

async function onUpdateCategory() {
  const formData = new FormData()
  if (categoryEditPictureRef.value?.files[0]) {
    formData.append('picture', categoryEditPictureRef.value.files[0])
  }
  formData.set('name', categoryToEdit.value.name)

  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchCategories()
}

onBeforeMount(fetchCategories)
</script>

<template>
  <div>
    <h3>Категории</h3>

    <form @submit.prevent.stop="onCategoryAdd">
      <input type="text" v-model="categoryToAdd.name" placeholder="Название" required />
      <input type="file" ref="categoriesPictureRef" @change="categoriesAddPictureChange" />
      <img :src="categoryAddImageUrl" style="max-height: 60px;" alt="">
      <button>Добавить</button>
    </form>

    <div v-for="item in categories" :key="item.id" class="item">
      <div>{{ item.name }}</div>

      <!-- Картинка: клик → открыть модалку просмотра -->
      <div v-if="item.picture">
        <img :src="item.picture"
             style="max-height: 60px; cursor: pointer;"
             @click="onImageClick(item)"
             data-bs-toggle="modal"
             data-bs-target="#viewImageModal" />
      </div>

      <button @click="onCategoryEditClick(item)" data-bs-toggle="modal" data-bs-target="#editCategoryModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
    </div>

    <!-- Модалка редактирования -->
    <div class="modal fade" id="editCategoryModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" v-model="categoryToEdit.name" placeholder="Название" />
            <input type="file" ref="categoryEditPictureRef" @change="categoriesEditPictureChange" />
            <img :src="categoryEditImageUrl" style="max-height: 60px;" alt="">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateCategory">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модалка просмотра картинки -->
    <div class="modal fade" id="viewImageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-body text-center">
            <img :src="viewImageUrl" style="max-width: 100%; max-height: 80vh;" alt="" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item { margin-bottom: 5px; }
</style>