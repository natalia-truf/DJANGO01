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

// Для галереи
const galleryPictureRef = ref()
const albumImages = ref([])
const selectedProductForAlbum = ref({})

// Для просмотра большой картинки
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

function onImageClick(url) {
  viewImageUrl.value = url
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
  formData.set('description', productToAdd.value.description || '')

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
  productToEdit.value = {
    ...product,
    category_id: product.category?.id ?? product.category,
    supplier_id: product.supplier?.id ?? product.supplier,
  }
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
  formData.set('description', productToEdit.value.description || '')

  await axios.put(`/api/products/${productToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  await fetchProducts()
}

// ========== Галерея ==========

function onOpenAlbum(product) {
  selectedProductForAlbum.value = product
  albumImages.value = product.images || []
}

async function onAddGalleryImage() {
  if (!galleryPictureRef.value?.files[0]) return

  const formData = new FormData()
  formData.append('picture', galleryPictureRef.value.files[0])
  formData.append('product', selectedProductForAlbum.value.id)

  await axios.post('/api/productimages/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  await fetchProducts()
  const updated = products.value.find(p => p.id === selectedProductForAlbum.value.id)
  if (updated) {
    selectedProductForAlbum.value = updated
    albumImages.value = updated.images
  }
  galleryPictureRef.value.value = ''
}

async function onRemoveGalleryImage(image) {
  await axios.delete(`/api/productimages/${image.id}/`)
  await fetchProducts()
  const updated = products.value.find(p => p.id === selectedProductForAlbum.value.id)
  if (updated) {
    selectedProductForAlbum.value = updated
    albumImages.value = updated.images
  }
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

    <!-- Форма добавления -->
    <form @submit.prevent.stop="onProductAdd">
      <input type="text" v-model="productToAdd.name" placeholder="Название" required />
      <input type="number" v-model="productToAdd.price" placeholder="Цена" required />
      <select v-model="productToAdd.category_id" required>
        <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
      </select>
      <select v-model="productToAdd.supplier_id" required>
        <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
      </select>
      <input type="text" v-model="productToAdd.description" placeholder="Описание" />
      <input type="file" ref="productsPictureRef" @change="productsAddPictureChange" />
      <img :src="productAddImageUrl" style="max-height: 60px;" alt="">
      <button>Добавить</button>
    </form>

    <!-- Список товаров -->
    <div v-for="item in products" :key="item.id" class="item">
      <div>{{ item.name }} — {{ item.price }} руб. — {{ item.category?.name }}</div>

      <div v-if="item.picture">
        <img :src="item.picture"
             style="max-height: 60px; cursor: pointer;"
             @click="onImageClick(item.picture)"
             data-bs-toggle="modal"
             data-bs-target="#viewImageModal" />
      </div>

      <button @click="onProductEditClick(item)" data-bs-toggle="modal" data-bs-target="#editProductModal">
        Редактировать
      </button>
      <button @click="onRemoveClick(item)">Удалить</button>
      <button @click="onOpenAlbum(item)" data-bs-toggle="modal" data-bs-target="#albumModal">
        Альбом ({{ item.images?.length || 0 }})
      </button>
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
            <div>
              <input type="text" v-model="productToEdit.name" placeholder="Название" />
            </div>
            <div>
              <input type="number" v-model="productToEdit.price" placeholder="Цена" />
            </div>
            <div>
              <select v-model="productToEdit.category_id">
                <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div>
              <select v-model="productToEdit.supplier_id">
                <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
              </select>
            </div>
            <div>
              <input type="text" v-model="productToEdit.description" placeholder="Описание" />
            </div>
            <div>
              <input type="file" ref="productEditPictureRef" @change="productsEditPictureChange" />
              <img :src="productEditImageUrl" style="max-height: 60px;" alt="">
            </div>
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

    <!-- Модалка просмотра одной картинки -->
    <div class="modal fade" id="viewImageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-body text-center">
            <img :src="viewImageUrl" style="max-width: 100%; max-height: 80vh;" alt="" />
          </div>
        </div>
      </div>
    </div>

    <!-- Модалка альбома -->
    <div class="modal fade" id="albumModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Альбом: {{ selectedProductForAlbum.name }}</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <input type="file" ref="galleryPictureRef" />
              <button @click="onAddGalleryImage">Добавить фото</button>
            </div>

            <div class="d-flex flex-wrap">
              <div v-for="img in albumImages" :key="img.id" style="margin: 5px;">
                <img :src="img.picture"
                     style="max-height: 100px; cursor: pointer;"
                     @click="onImageClick(img.picture)"
                     data-bs-toggle="modal"
                     data-bs-target="#viewImageModal" />
                <button  @click="onRemoveGalleryImage(img)">✖</button>
              </div>
            </div>

            <div v-if="albumImages.length === 0">Фото пока нет</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item {
  margin-bottom: 10px;
  padding: 5px;
  border-bottom: 1px solid #eee;
}
</style>