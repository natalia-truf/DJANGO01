<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const products = ref([])
const categories = ref([])
const suppliers = ref([])
const productToAdd = ref({})
const productToEdit = ref({})
const productsPictureRef = ref()
const productAddImageUrl = ref()
const productEditPictureRef = ref()
const productEditImageUrl = ref()

// Для просмотра картинки
const viewImageUrl = ref()

async function fetchProducts() {
  const r = await axios.get('/api/products/')
  products.value = r.data
}

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

async function fetchSuppliers() {
  const r = await axios.get('/api/suppliers/')
  suppliers.value = r.data
}

function productsAddPictureChange() {
  productAddImageUrl.value = URL.createObjectURL(productsPictureRef.value.files[0])
}

function productsEditPictureChange() {
  productEditImageUrl.value = URL.createObjectURL(productEditPictureRef.value.files[0])
}

// Открытие картинки для просмотра
function onImageClick(product) {
  viewImageUrl.value = product.picture
}

async function onProductAdd() {
  const formData = new FormData()
  if (productsPictureRef.value?.files[0]) {
    formData.append('picture', productsPictureRef.value.files[0])
  }
  formData.set('name', productToAdd.value.name)
  formData.set('price', productToAdd.value.price)
  formData.set('category_id', productToAdd.value.category_id)
  formData.set('supplier_id', productToAdd.value.supplier_id)

  await axios.post("/api/products/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchProducts()
}

async function onRemoveClick(product) {
  await axios.delete(`/api/products/${product.id}/`)
  await fetchProducts()
}

function onProductEditClick(product) {
  productToEdit.value = { ...product }
  productEditImageUrl.value = product.picture
}

async function onUpdateProduct() {
  const formData = new FormData()
  if (productEditPictureRef.value?.files[0]) {
    formData.append('picture', productEditPictureRef.value.files[0])
  }
  formData.set('name', productToEdit.value.name)
  formData.set('price', productToEdit.value.price)
  formData.set('category_id', productToEdit.value.category_id)
  formData.set('supplier_id', productToEdit.value.supplier_id)

  await axios.put(`/api/products/${productToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchProducts()
}

onBeforeMount(() => {
  fetchProducts()
  fetchCategories()
  fetchSuppliers()
})
</script>

<template>
  <div>
    <h3>Товары</h3>

    <form @submit.prevent.stop="onProductAdd">
      <input type="text" v-model="productToAdd.name" placeholder="Название" required />
      <input type="number" v-model="productToAdd.price" placeholder="Цена" required />
      <select v-model="productToAdd.category_id" required>
        <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
      </select>
      <select v-model="productToAdd.supplier_id" required>
        <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
      </select>
      <input type="file" ref="productsPictureRef" @change="productsAddPictureChange" />
      <img :src="productAddImageUrl" style="max-height: 60px;" alt="">
      <button>Добавить</button>
    </form>

    <div v-for="item in products" :key="item.id" class="item">
      <div>{{ item.name }} — {{ item.price }} руб.</div>

      <!-- Картинка: клик → открыть модалку просмотра -->
      <div v-if="item.picture">
        <img :src="item.picture"
             style="max-height: 60px; cursor: pointer;"
             @click="onImageClick(item)"
             data-bs-toggle="modal"
             data-bs-target="#viewImageModal" />
      </div>

      <button @click="onProductEditClick(item)" data-bs-toggle="modal" data-bs-target="#editProductModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
    </div>

    <!-- Модалка редактирования -->
    <div class="modal fade" id="editProductModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" v-model="productToEdit.name" placeholder="Название" />
            <input type="number" v-model="productToEdit.price" placeholder="Цена" />
            <select v-model="productToEdit.category_id">
              <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
            </select>
            <select v-model="productToEdit.supplier_id">
              <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
            </select>
            <input type="file" ref="productEditPictureRef" @change="productsEditPictureChange" />
            <img :src="productEditImageUrl" style="max-height: 60px;" alt="">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateProduct">
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