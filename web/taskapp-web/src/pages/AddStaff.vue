<template lang="pug">
.add-staff-container.p-10.w-200.mx-auto.max-w-lg
  h1.text-2xl.font-bold.mb-6 新規スタッフ登録

  .form-wrapper.bg-white.p-8.rounded-lg.shadow-md
    form(@submit.prevent="submitForm")
      //- 職員コード入力欄
      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="staff-code") 職員コード
        input#staff-code.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(
          type="text"
          v-model.trim="staffCode"
          placeholder="半角数字6桁で入力"
          required
          maxlength="6"
          pattern="^[0-9]{6}$"
        )
        p.text-xs.text-gray-500.mt-1 例: 001234

      //- 氏名入力欄
      .mb-8
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="staff-name") 氏名
        input#staff-name.shadow.appearance-none.border.rounded.w-full.py-2.px-3.text-gray-700.leading-tight(
          type="text"
          v-model.trim="staffName"
          placeholder="山田 太郎"
          required
        )

      //- ボタンエリア
      .flex.items-center.justify-end
        //- キャンセルボタン
        button.bg-gray-500.hover_bg-gray-700.text-white.font-bold.py-2.px-4.rounded.mr-4.border-none(
          type="button"
          @click="goBackToList"
        ) 戻る

        //- 登録ボタン
        button.bg-blue-500.hover_bg-blue-700.text-white.font-bold.py-2.px-4.rounded.border-none(
          type="submit"
          :disabled="isSubmitting"
          :class="{ 'opacity-50 cursor-not-allowed': isSubmitting }"
        )
          span(v-if="isSubmitting") 登録中...
          //-isSubmittingがtrueの間ボタンを無効化
          span(v-else) 登録
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import { STAFF_BASE_URL } from '@/utils/endpoints'

// ルーターとトースト通知のインスタンスを取得
const router = useRouter()
const toast = useToast()

// フォームの入力値を保持するリアクティブな変数
const staffCode = ref<string>('')
const staffName = ref<string>('')
const isSubmitting = ref<boolean>(false) // 送信中の状態を管理

// フォームの送信処理
const submitForm = async () => {
  if (!staffCode.value || !staffName.value) {
    toast.error('全ての項目を入力してください。', { timeout: 2000 })
    return
  }
  // 6桁の数字であるかの正規表現チェック
  if (!/^[0-9]{6}$/.test(staffCode.value)) {
    toast.error('職員コードは6桁の数字で入力してください。', { timeout: 2000 })
    return
  }

  isSubmitting.value = true

  try {
    // バックエンドAPIに送信するデータを作成
    const payload = {
      code: staffCode.value,
      name: staffName.value,
    }
    console.log(staffCode.value)
    console.log(staffName.value)
    // 作成したバックエンドAPIのエンドポイントにPOSTリクエストを送信
    await axios.post(`${STAFF_BASE_URL}/`, payload)

    // 成功した場合
    toast.success('新しいスタッフを登録しました！', { timeout: 1600 })
    router.push('/staffs') // 登録後は一覧ページに戻る
  } catch (error) {
    console.error('スタッフの登録に失敗しました:', error)
    if (axios.isAxiosError(error) && error.response) {
      // バックエンドから返されたエラーメッセージを表示
      toast.error(error.response.data.detail || '登録に失敗しました。', { timeout: 2000 })
      console.log(error.response.data.detail)
    } else {
      toast.error('スタッフの登録中にエラーが発生しました。', { timeout: 2000 })
    }
  } finally {
    isSubmitting.value = false
  }
}

const goBackToList = () => {
  router.push('/staffs')
}
</script>

<style lang="scss" scoped>
// .add-staff-container {
//   max-width: auto;
//   margin-left: 20rem;
//   margin-right: 20rem;
// }
</style>
