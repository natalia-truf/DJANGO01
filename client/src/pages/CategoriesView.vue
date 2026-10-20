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
function onImageClick(url) {
  viewImageUrl.value = url
}
async function onCategoryAdd() {
  const formData = new FormData()
  if (categoriesPictureRef.value?.files[0]) formData.append('picture', categoriesPictureRef.value.files[0])
  formData.set('name', categoryToAdd.value.name)
  await axios.post("/api/categories/", formData, { headers: { 'Content-Type': 'multipart/form-data' } })
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
  if (categoryEditPictureRef.value?.files[0]) formData.append('picture', categoryEditPictureRef.value.files[0])
  formData.set('name', categoryToEdit.value.name)
  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
  await fetchCategories()
}

onBeforeMount(fetchCategories)
</script>

<template>
  <div>
    <h3 class="mb-4">Категории</h3>

    <form @submit.prevent.stop="onCategoryAdd" class="mb-4">
      <div class="row g-2">
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="categoryToAdd.name" required />
          <label>Название</label>
        </div></div>
        <div class="col-auto">
          <input class="form-control" type="file" ref="categoriesPictureRef" @change="categoriesAddPictureChange" />
        </div>
        <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
      </div>
    </form>

    <div v-for="item in categories" :key="item.id" class="border rounded p-3 mb-2">
      <div class="row align-items-center">
        <div class="col-6">{{ item.name }}</div>
        <div class="col-3 text-end">
          <img v-if="item.picture" :src="item.picture" style="max-height: 60px;" class="rounded"
               @click="onImageClick(item.picture)" data-bs-toggle="modal" data-bs-target="#viewImageModal" />
        </div>
        <div class="col-3 d-flex gap-3 justify-content-center">
          <button class="btn btn-success" @click="onCategoryEditClick(item)" data-bs-toggle="modal" data-bs-target="#editCategoryModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editCategoryModal" tabindex="-1">
      <div class="modal-dialog"><div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="categoryToEdit.name" /><label>Название</label>
          </div>
          <input type="file" class="form-control" ref="categoryEditPictureRef" @change="categoriesEditPictureChange" />
          <img :src="categoryEditImageUrl" style="max-height: 60px;" class="rounded mt-2" alt="">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateCategory">Сохранить</button>
        </div>
      </div></div>
    </div>

    <div class="modal fade" id="viewImageModal" tabindex="-1">
      <div class="modal-dialog modal-lg"><div class="modal-content">
        <div class="modal-body text-center">
          <img :src="viewImageUrl" class="img-fluid rounded" style="max-height: 80vh;" alt="" />
        </div>
      </div></div>
    </div>
  </div>
</template>