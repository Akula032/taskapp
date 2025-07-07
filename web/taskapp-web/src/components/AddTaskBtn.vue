<template lang="pug">
button.border-none.bg-blue-500.hover-bg-blue-600.font-semibold.rounded-md.shadow-sm.my-4.ml-10.py-2.text-center.w-32(
  @click="navigateToAddTask"
  ) + タスクを追加
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
const navigateToAddTask = () => {
  router.push({ name: 'AddTask' })
}
</script>

<style lang="scss" scoped></style>
