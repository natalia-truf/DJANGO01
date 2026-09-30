<script setup>
import { ref } from 'vue';

let a = ref(13);
let b = ref(23);
</script>

<template>
  <div>
    <input type="number" v-model="a"><br>
    <input type="number" v-model="b">
    <br>
    <b>{{ a }} + {{ b }}</b> <span>= {{ a + b }}</span>
  </div>
</template>