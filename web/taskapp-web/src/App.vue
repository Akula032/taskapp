<template lang="pug">
.app-layout
  AppHeader
  RouterView
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from './layout/Header.vue'
</script>

<style lang="scss" scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
