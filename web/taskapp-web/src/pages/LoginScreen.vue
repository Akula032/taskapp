<template lang="pug">
  .login-container
    .login-box
      h1.pt-10 ログイン
      .input-group.mt-10
        label(for="username") 職員ID:
        input(type="text" id="username" v-model="username")
      .input-group.mt-10
        label(for="password") パスワード:
        input(type="password" id="password" v-model="password")
      p.error-message(v-if="errorMessage") {{ errorMessage }}
      button.login-button.mt-10 ログイン
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { LOGIN_BASE_URL } from '@/utils/endpoints'
const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const response = await axios.post(`${LOGIN_BASE_URL}`, {
      code: username.value,
      password: password.value,
    })

    router.push({ name: 'Attendance' })
  } catch (error) {
    isLoading.value = false
    if (axios.isAxiosError(error)) {
      if (error.response) {
        errorMessage.value =
          error.response.data?.detail ||
          `エラー (${error.response.status}): IDまたはパスワードが違います。`
      } else if (error.request) {
        errorMessage.value = 'サーバーに接続できませんでした'
      }
    } else {
      errorMessage.value = '予期せぬエラーが発生しました'
    }
  }
}
</script>
<style scoped></style>
