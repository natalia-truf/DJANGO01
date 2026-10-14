<script setup>
import { onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'
import Navbar from '@/components/Navbar.vue'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
})
</script>

<template>
  <Navbar />

  <div class="container-fluid px-4">
    <router-view />
  </div>
</template>