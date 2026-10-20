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
const galleryPictureRef = ref()
const albumImages = ref([])
const selectedProductForAlbum = ref({})
const viewImageUrl = ref()

async function fetchProducts() {
  products.value = (await axios.get('/api/products/')).data
}
async function fetchCategories() {
  categories.value = (await axios.get('/api/categories/')).data
}
async function fetchSuppliers() {
  suppliers.value = (await axios.get('/api/suppliers/')).data
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
  const fd = new FormData()
  if (productsPictureRef.value?.files[0]) fd.append('picture', productsPictureRef.value.files[0])
  fd.set('name', productToAdd.value.name)
  fd.set('price', productToAdd.value.price)
  fd.set('category_id', productToAdd.value.category_id)
  fd.set('supplier_id', productToAdd.value.supplier_id)
  fd.set('description', productToAdd.value.description || '')
  await axios.post('/api/products/', fd)
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
  const fd = new FormData()
  if (productEditPictureRef.value?.files[0]) fd.append('picture', productEditPictureRef.value.files[0])
  fd.set('name', productToEdit.value.name)
  fd.set('price', productToEdit.value.price)
  fd.set('category_id', productToEdit.value.category_id)
  fd.set('supplier_id', productToEdit.value.supplier_id)
  fd.set('description', productToEdit.value.description || '')
  await axios.put(`/api/products/${productToEdit.value.id}/`, fd)
  await fetchProducts()
}

function onOpenAlbum(product) {
  selectedProductForAlbum.value = product
  albumImages.value = product.images || []
}

async function refreshAlbum() {
  await fetchProducts()
  const updated = products.value.find(p => p.id === selectedProductForAlbum.value.id)
  if (updated) {
    selectedProductForAlbum.value = updated
    albumImages.value = updated.images
  }
}

async function onGalleryFileChange() {
  if (!galleryPictureRef.value?.files[0]) return
  const fd = new FormData()
  fd.append('picture', galleryPictureRef.value.files[0])
  fd.append('product', selectedProductForAlbum.value.id)
  await axios.post('/api/productimages/', fd)
  await refreshAlbum()
  galleryPictureRef.value.value = ''
}

async function onRemoveGalleryImage(image) {
  await axios.delete(`/api/productimages/${image.id}/`)
  await refreshAlbum()
}

onBeforeMount(() => {
  fetchProducts()
  fetchCategories()
  fetchSuppliers()
})
</script>

<template>
  <div>
    <h3 class="mb-4">Товары</h3>

    <form @submit.prevent.stop="onProductAdd" class="mb-4">
      <div class="row g-2">
        <div class="col"><div class="form-floating">
          <input type="text" class="form-control" v-model="productToAdd.name" required />
          <label>Название</label>
        </div></div>
        <div class="col"><div class="form-floating">
          <input type="number" step="0.01" class="form-control" v-model="productToAdd.price" required />
          <label>Цена</label>
        </div></div>
        <div class="col-auto">
          <input class="form-control" type="file" ref="productsPictureRef" @change="productsAddPictureChange" />
        </div>
        <div class="col-auto"><div class="form-floating">
          <select class="form-select" v-model="productToAdd.category_id" required>
            <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
          </select>
          <label>Категория</label>
        </div></div>
        <div class="col-auto"><div class="form-floating">
          <select class="form-select" v-model="productToAdd.supplier_id" required>
            <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
          </select>
          <label>Поставщик</label>
        </div></div>
        <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
      </div>
    </form>

    <div v-for="item in products" :key="item.id" class="border rounded p-3 mb-2">
      <div class="row align-items-center">
        <div class="col-3">{{ item.name }}</div>
        <div class="col-2 text-end">{{ item.price }} руб.</div>
        <div class="col-2 text-end">{{ item.category?.name }}</div>

        <div class="col-2 text-end">
          <img v-if="item.picture" :src="item.picture" style="max-height: 60px;" class="rounded"
               @click="onImageClick(item.picture)" data-bs-toggle="modal" data-bs-target="#viewImageModal" />
        </div>

        <div class="col-3 d-flex gap-2 justify-content-center">
          <button class="btn btn-success" @click="onProductEditClick(item)" data-bs-toggle="modal" data-bs-target="#editProductModal">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
          <button class="btn btn-primary" @click="onOpenAlbum(item)" data-bs-toggle="modal" data-bs-target="#albumModal">
            Альбом ({{ item.images?.length || 0 }})
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editProductModal" tabindex="-1">
      <div class="modal-dialog"><div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="productToEdit.name" /><label>Название</label>
          </div>
          <div class="form-floating mb-2">
            <input type="number" step="0.01" class="form-control" v-model="productToEdit.price" /><label>Цена</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="productToEdit.category_id">
              <option :value="c.id" v-for="c in categories" :key="c.id">{{ c.name }}</option>
            </select><label>Категория</label>
          </div>
          <div class="form-floating mb-2">
            <select class="form-select" v-model="productToEdit.supplier_id">
              <option :value="s.id" v-for="s in suppliers" :key="s.id">{{ s.name }}</option>
            </select><label>Поставщик</label>
          </div>
          <input type="file" class="form-control" ref="productEditPictureRef" @change="productsEditPictureChange" />
          <img :src="productEditImageUrl" style="max-height: 60px;" class="rounded mt-2" alt="">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateProduct">Сохранить</button>
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

    <div class="modal fade" id="albumModal" tabindex="-1">
      <div class="modal-dialog modal-lg"><div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Альбом: {{ selectedProductForAlbum.name }}</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">

          <div class="d-flex gap-2 mb-3">
            <input type="file" class="form-control" ref="galleryPictureRef" @change="onGalleryFileChange" />
            <button type="button" class="btn btn-primary" @click="galleryPictureRef.click()">Добавить фото</button>
          </div>

          <div v-if="albumImages.length > 0">
            <div :key="albumImages.length" id="albumCarousel" class="carousel slide">
              <div class="carousel-inner">
                <div v-for="(img, index) in albumImages"
                     :key="img.id"
                     class="carousel-item"
                     :class="{ active: index === 0 }">
                  <img :src="img.picture" class="d-block w-100" style="max-height: 400px; object-fit: contain;" />
                  <div class="text-center mt-2">
                    <button class="btn btn-danger" @click="onRemoveGalleryImage(img)">Удалить это фото</button>
                  </div>
                </div>
              </div>

              <button class="carousel-control-prev" type="button" data-bs-target="#albumCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
                <span class="visually-hidden">Предыдущий</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#albumCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
                <span class="visually-hidden">Следующий</span>
              </button>
            </div>
          </div>

          <div v-else>Фото пока нет</div>

        </div>
      </div></div>
    </div>
  </div>
</template>