<script setup>
import { onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
})
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/products">Товары</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/categories">Категории</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/suppliers">Поставщики</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/points">Точки продажи</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/orders">Заказы</router-link>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              Пользователь
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><a class="dropdown-item" href="/admin" target="_blank">Админка</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container-fluid px-4">
    <router-view />
  </div>
</template>