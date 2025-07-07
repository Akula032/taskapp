<template lang="pug">
//- .fixed.top-0.z-10 上部固定で、最前面表示
.main-header.bg-gray.py-6.pl-10.fixed.top-0.z-10
  .text-white.flex.justify-between.items-center
    h1.hover-text-gray-300.text-size-10(tabindex='0' @click="moveToMain()") タスク管理システム
    .nav-group
      //- RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/attendance") 打刻
      //- RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/login") ログイン
      RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/taskapp") タスク一覧
      RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/calendar") カレンダー
      RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/staffs") スタッフ一覧
      //- RouterLink.hover-text-gray-300.text-white.text-size-5.mr-8(to="/staffs/add") スタッフ追加
</template>

<script setup lang="ts">
import router from '@/router'
import { RouterLink } from 'vue-router' //Homeを使う時インポート
const moveToMain = () => {
  router.push({ path: '/taskapp' })
}
</script>

<style lang="scss" scoped>
.main-header {
  // position: fixed;
  position: sticky;
}
</style>
