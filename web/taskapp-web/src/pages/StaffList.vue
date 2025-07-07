<template lang="pug">
.staff-list-container.p-10
  h1.text-2xl.font-bold.mb-6 職員一覧
  //- 新規追加ページへのボタン
  .mb-6
    RouterLink.bg-blue-500.hover-bg-blue-700.text-white.font-bold.py-2.px-4.rounded(to="/staffs/add") 新規追加
  //- ロード中の表示
  .loading(v-if="isLoading")
    p 読み込み中...
  //- エラーメッセージの表示
  .error(v-else-if="errorMessage")
    p.text-red-500 {{ errorMessage }}
  .table-container(v-else)
    table.min-w-full.bg-white
      thead
        tr
          th.py-2.px-4.text-center.bg-slate-100 職員コード
          th.py-2.px-4.text-center.bg-slate-100 氏名
          th.py-2.px-4.text-center.bg-slate-100 操作
      tbody
        tr.tabletext(v-for="staff in staffList" :key="staff.id")
          td.py-2.px-4.text-center {{ staff.code }}
          td.py-2.px-4.text-center {{ staff.name }}
          td.py-2.px-4.text-center
            button.bg-green-500.hover-bg-green-600.text-white.text-sm.py-1.px-3.rounded.mr-2.border-none(@click="openEditModal(staff)") 編集
            button.bg-red-500.hover-bg-red-600.text-white.text-sm.py-1.px-3.rounded.border-none(@click="openDeleteModal(staff)") 削除
  StaffEditModal(
    :is-visible="isEditModalVisible"
    :staff-to-edit="selectedStaff"
    @close="closeEditModal"
    @save="handleSaveStaff"
  )
  DeleteModal(
    :is-visible="isDeleteModalVisible"
    :task-title="staffToDelete ? staffToDelete.name : null"
    @close="closeDeleteModal"
    @confirm-delete="handleConfirmDelete"
  )
</template>

<script setup lang="ts">
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { STAFF_BASE_URL } from '@/utils/endpoints'
import StaffEditModal from '@/components/StaffEditModal.vue'
import DeleteModal from '@/components/DeleteModal.vue'
import type { Staff } from '@/utils/interface.ts'

const toast = useToast()

const staffList = ref<Staff[]>([]) // スタッフのリストを保持
const isLoading = ref<boolean>(false) // ローディング状態を管理
const errorMessage = ref<string>('') // エラーメッセージを保持

const isEditModalVisible = ref<boolean>(false) // モーダルの表示状態
const selectedStaff = ref<Staff | null>(null)

const isDeleteModalVisible = ref<boolean>(false)
const staffToDelete = ref<Staff | null>(null)

//Get処理
const fetchStaffs = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await axios.get<Staff[]>(`${STAFF_BASE_URL}`)
    staffList.value = response.data
    console.log(staffList.value)
  } catch (error) {
    console.error('スタッフの読み込みに失敗しました:', error)
    // axiosからのHTTPエラーであり、かつ サーバーからのレスポンス情報を含んでいることを確認
    if (axios.isAxiosError(error) && error.response) {
      // バックエンドから返されたエラーメッセージ (detail) を表示
      errorMessage.value = error.response.data.detail || 'サーバーでエラーが発生しました。'
    } else {
      // ネットワークエラーなど、axios以外の予期せぬエラー
      errorMessage.value = 'スタッフ一覧の読み込みに失敗しました。'
    }
  } finally {
    isLoading.value = false
  }
}

const openEditModal = (staff: Staff) => {
  selectedStaff.value = staff
  isEditModalVisible.value = true
}
const closeEditModal = () => {
  isEditModalVisible.value = false
  selectedStaff.value = null
}

const openDeleteModal = (staff: Staff) => {
  staffToDelete.value = staff
  isDeleteModalVisible.value = true
}
const closeDeleteModal = () => {
  isDeleteModalVisible.value = false
  staffToDelete.value = null
}

//編集PATCH
const handleSaveStaff = async (updatedStaff: Staff) => {
  if (!updatedStaff) return

  try {
    const payload = {
      code: updatedStaff.code,
      name: updatedStaff.name,
    }
    // バックエンドの編集APIを呼び出す
    await axios.patch(`${STAFF_BASE_URL}/${updatedStaff.id}`, payload)
    console.log(payload)

    toast.success('スタッフ情報を更新しました！', { timeout: 1600 })
    closeEditModal() // モーダルを閉じる
    await fetchStaffs() // 一覧を再読み込みして表示を更新
  } catch (error) {
    console.error('スタッフ情報の更新に失敗しました:', error)
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`更新に失敗しました: ${error.response.data.detail}`, { timeout: 2000 })
    }
  }
}

//削除PATCH
const handleConfirmDelete = async () => {
  if (!staffToDelete.value) return

  try {
    // バックエンドの非アクティブ化APIを呼び出す
    await axios.patch(`${STAFF_BASE_URL}/${staffToDelete.value.id}/deactivate`)
    toast.success(`${staffToDelete.value.name}さんを削除しました。`, { timeout: 1600 })
    closeDeleteModal()
    await fetchStaffs() // 一覧を再読み込み
  } catch (error) {
    console.error('スタッフの削除に失敗しました:', error)
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`処理に失敗しました: ${error.response.data.detail}`, { timeout: 2000 })
    }
  }
}

onMounted(() => {
  fetchStaffs()
  console.log('/staffをマウント')
})
</script>

<style lang="scss" scoped>
.staff-list-container {
  // max-width: 800px;
  margin-left: 10rem;
  margin-right: 10rem;
}
.tabletext {
  border: 1px solid black;
}
</style>
