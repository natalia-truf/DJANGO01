<script setup>
import { onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
})
</script>

<template>
  <nav>
    <router-link to="/categories">Категории</router-link> |
    <router-link to="/suppliers">Поставщики</router-link> |
    <router-link to="/points">Точки продажи</router-link> |
    <router-link to="/products">Товары</router-link> |
    <router-link to="/orders">Заказы</router-link> |

    <!-- Кнопка входа в админку -->
    <a href="/admin">Админка</a>
  </nav>

  <hr>

  <router-view />
</template>