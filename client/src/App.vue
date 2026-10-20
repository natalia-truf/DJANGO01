<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <nav-bar></nav-bar>
  <div class="container-fluid px-4 px-md-5 mt-4">
    <router-view></router-view>
  </div>
</template>

<style scoped></style>