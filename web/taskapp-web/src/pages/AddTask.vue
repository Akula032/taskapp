<template lang="pug">
.add-task-page(class="py-8 px-4 md:px-6 lg:px-8")
  .add-task-container.max-w-xl.mx-auto.bg-white.p-6.md-p-8.rounded-lg.shadow-xl
    h2.font-bold 新しいタスクを追加
    form(@submit.prevent="handleAddTask")
      .mb-8
        input#task-title.shadow.appearance-none.border-none.w-140.py-3.text-gray-700.outline-none.pl-2(
          type="text"
          v-model.trim="formState.detailName"
          placeholder="タスクカードのタイトルを入力"
          autocomplete="off"
          required
        )
      div(class="flex space-x-4")
        //-タスクグループ
        .taskgroup.mb-5.w-full.mr-10
          label.block.text-gray-700.text-sm.font-bold(for="task-group-input") タスク (縦の列になります)
          .relative
            input#task-group-input.p-3.rounded.border.border-gray-300.shadow.focus-outline-none.focus-ring-2.focus-ring-blue-500.focus-border-transparent(
              type="text"
              placeholder="選択または入力"
              v-model.trim="formState.taskGroupInput"
              @input="onTaskGroupInput"
              @focus="showTaskGroupDropdown = true"
              @blur="hideTaskGroupDropdown"
              autocomplete="off"
              required
            )
            ul(v-if="showTaskGroupDropdown && taskGroupList.length" class="absolute border bg-gray-200 w-60 z-20 max-h-40 overflow-auto")
              li(
                  v-for="item in taskGroupList"
                  :key="item.id"
                  @mousedown.prevent="selectItem(item)"
                  class="px-2 py-1 hover:bg-blue cursor-pointer"
                ) {{ item.name }}
          //- カテゴリのドロップダウン
        .category.w-full
          label.block.text-gray-700.text-sm.font-bold(for="category-input") カテゴリー
          .relative
            input#category-input.p-3.rounded.border.border-gray-300.shadow.focus-outline-none.focus-ring-2.focus-ring-blue-500.focus-border-transparent(
              type="text"
              placeholder="選択または入力"
              v-model="formState.categoryInput"
              @input="onCategoryInput"
              @focus="showCategoryDropdown = true"
              @blur="hideCategoryDropdown"
              autocomplete="off"
              required
            )
            ul(v-if="showCategoryDropdown && categoryList.length" class="absolute border bg-gray-200 w-60 z-10 max-h-40 overflow-auto")
              li(
                v-for="item in categoryList"
                :key="item.id"
                @mousedown.prevent="selectCategoryItem(item)"
                class="px-2 py-1 hover:bg-blue cursor-pointer"
              ) {{ item.name }}
      //-日付のinput
      .flex.space-x-4.mb-6
        .start-day.mr-10
          label.block.text-gray-700.text-sm.font-bold.mb-2(for="start-date") 開始日（任意）
          input#start-date.w-full.p-2.rounded.border.border-gray-300(
            type="date"
            v-model="formState.startDate"
          )
        .end-day
          label.block.text-gray-700.text-sm.font-bold.mb-2(for="end-date") 終了日（任意）
          input#end-date.w-full.p-2.rounded.border.border-gray-300(
            type="date"
            v-model="formState.endDate"
          )
      .staff.mb-6
        label.block.text-gray-700.text-sm.font-bold(for="staff-select") 担当スタッフ
        select#staff-select.w-full.p-3.rounded.border.border-gray-300(
          v-model="formState.selectedStaffId"
          required
        )
          option(:value="null" disabled) 担当者を選択してください
          option(
            v-for="staff in staffList"
            :key="staff.id"
            :value="staff.id"
          ) {{ staff.name }}
      .priority.mb-6
        label.block.text-gray-700.text-sm.font-bold(for="priority-select") 優先度
        select#priority-select.w-full.p-3.rounded.border.border-gray-300(
          v-model="formState.selectedPriorityId"
          required
        )
          option(:value="null" disabled) 優先度を選択してください
          option(
            v-for="priority in priorityList"
            :key="priority.id"
            :value="priority.id"
          ) {{ priority.importance }}
            .flex.space-x-4.mb-6
      .status-button.mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-3 ステータス
        .flex.justify-center.space-x-8
          label.flex.items-center.cursor-pointer(
            v-for="status in statusList"
            :key="status.id"
            :for="'status-' + status.id"
          )
            input(
              type="radio"
              name="task-status"
              v-model="formState.selectedStatusId"
              :id="'status-' + status.id"
              :value="status.id"
              class="h-5 w-5"
            )
            span.ml-2.text-gray-800 {{ status.name }}
      //-アクションボタン
      .flex.items-center.justify-center.space-x-4
        button.bg-gray-200.hover-bg-gray-300.text-gray-700.font-semibold.py-2.px-5.rounded-md.transition-colors.focus-outline-none.mt-4.mr-15.border-none(
          type="button"
          @click="cancel"
        ) キャンセル
        button.bg-blue-500.hover-bg-blue-600.text-white.font-semibold.py-2.px-5.rounded-md.transition-colors.focus-outline-none.mt-4.border-none(
          :disabled="isLoading"
          :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
          type="submit"
        ) {{ isLoading ? '追加中...' : 'タスクを追加' }}
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import {
  TASK_DETAIL_BASE_URL,
  STATUSES_BASE_URL,
  CATEGORY_BASE_URL,
  STAFF_BASE_URL,
  PRIORITY_BASE_URL,
} from '@/utils/endpoints'
import type { Base, TaskWithCategory, Payload, Priority } from '@/utils/interface'

const showTaskGroupDropdown = ref(false)

// interface Base {
//   id: number
//   name: string
// }

// interface TaskWithCategory {
//   //さっきの新しいやつ
//   id: number
//   title: string
//   category: Base
// }
// interface Payload {
//   detail_name: string
//   status_id: number
//   staff_id: number
//   priority_id: number
//   task_id?: number
//   new_task_title?: string
//   category_id?: number
//   new_category_name?: string
//   start_date?: string | null
//   end_date?: string | null
// }
// interface Priority {
//   id: number
//   importance: string
// }

const router = useRouter()
const toast = useToast()

// 状態管理
const isLoading = ref(false)

const formState = reactive({
  detailName: '',
  categoryInput: '',
  taskGroupInput: '',
  selectedStatusId: 1,
  selectedStaffId: null as number | null,
  selectedPriorityId: 5 as number | null, //優先度の初期値は「優先度なし」
  startDate: null as string | null,
  endDate: null as string | null,
})
// 選択肢リスト
const categoryList = ref<Base[]>([]) // カテゴリのドロップダウンリスト
const taskGroupList = ref<Base[]>([]) // タスクのドロップダウンリスト
const statusList = ref<Base[]>([]) //ステータス一覧
const staffList = ref<Base[]>([]) // スタッフのリスト
const priorityList = ref<Priority[]>([]) // 優先度リスト
const rawTaskData = ref<TaskWithCategory[]>([]) // 既存タスク判定用に、生のデータを保持

//ライフサイクルとデータ取得
const fetchDataForForm = async () => {
  isLoading.value = true
  try {
    const [
      categoryResponse,
      tasksWithCategoryResponse,
      statusResponse,
      staffResponse,
      priorityResponse,
    ] = await Promise.all([
      axios.get<Base[]>(CATEGORY_BASE_URL),
      axios.get<TaskWithCategory[]>(`${TASK_DETAIL_BASE_URL}/with_category`),
      axios.get<Base[]>(STATUSES_BASE_URL),
      axios.get<Base[]>(STAFF_BASE_URL),
      axios.get<Priority[]>(PRIORITY_BASE_URL),
    ])

    // APIからのレスポンスをコンポーネントの状態にセット
    categoryList.value = categoryResponse.data.map((c) => ({ id: c.id, name: c.name }))
    statusList.value = statusResponse.data
    staffList.value = staffResponse.data
    priorityList.value = priorityResponse.data
    console.log('---重要度ドロップの値/priorityList---', priorityList.value)
    //APIレスポンスからタスクグループの選択肢を作成
    const tasksWithCategory = tasksWithCategoryResponse.data
    taskGroupList.value = tasksWithCategory.map((task) => ({
      id: task.id,
      name: task.title, // ドロップダウンの表示名として 'name' に統一
    }))
    // 既存タスク判定用の生データも更新
    rawTaskData.value = tasksWithCategory
  } catch (error) {
    toast.error('選択肢データの取得に失敗しました。', { timeout: 2000 })
  } finally {
    isLoading.value = false
  }
}

const onTaskGroupInput = () => {
  // タスクグループが入力されたときの処理
  showTaskGroupDropdown.value = true
}
// タスクグループのフォーカスが外れたときの処理
const hideTaskGroupDropdown = () => {
  // blur後すぐに候補をクリックできるよう setTimeout で遅延
  setTimeout(() => {
    showTaskGroupDropdown.value = false
  }, 100)
}
// タスクグループが選択されたときの処理
const selectItem = (item: Base) => {
  formState.taskGroupInput = item.name
  showTaskGroupDropdown.value = false
}

const showCategoryDropdown = ref(false)
// カテゴリーが入力されたときの処理
const onCategoryInput = () => {
  showCategoryDropdown.value = true
}
// カテゴリーのフォーカスが外れたときの処理
const hideCategoryDropdown = () => {
  setTimeout(() => {
    showCategoryDropdown.value = false
  }, 100)
}
// カテゴリーが選択されたときの処理
const selectCategoryItem = (item: Base) => {
  formState.categoryInput = item.name
  showCategoryDropdown.value = false
}

const handleAddTask = async () => {
  //後々入力データを送るだけにしたい
  if (
    !formState.detailName.trim() ||
    !formState.taskGroupInput.trim() ||
    !formState.categoryInput.trim() ||
    !formState.selectedStaffId ||
    !formState.selectedPriorityId
  ) {
    toast.error('全ての項目を入力または選択してください。', { timeout: 2000 })
    return
  }

  isLoading.value = true

  const payload: Payload = {
    detail_name: formState.detailName.trim(),
    status_id: formState.selectedStatusId,
    staff_id: formState.selectedStaffId, //選択したID
    priority_id: formState.selectedPriorityId, //選択した優先度
    start_date: formState.startDate,
    end_date: formState.endDate,
  }
  //ユーザーが選択/入力したカテゴリ情報を特定する
  const selectedCategory = categoryList.value.find((c) => c.name === formState.categoryInput)
  let existingTaskGroup = null
  if (selectedCategory) {
    // rawデータから、タイトルとカテゴリIDの両方が一致するものを探す
    existingTaskGroup = rawTaskData.value.find(
      (task) => task.title === formState.taskGroupInput && task.category.id === selectedCategory.id,
    )
  }
  //検索結果に基づいてペイロードを組み立てる
  if (existingTaskGroup) {
    // 既存の「タイトル」と「カテゴリ」の組み合わせが見つかった場合 -> IDを送る
    payload.task_id = existingTaskGroup.id
  } else {
    payload.new_task_title = formState.taskGroupInput.trim()
    if (selectedCategory) {
      payload.category_id = selectedCategory.id
    } else {
      payload.new_category_name = formState.categoryInput.trim()
    }
    console.log('---ペイロード---', payload)
  }

  try {
    await axios.post(TASK_DETAIL_BASE_URL, payload)
    toast.success('新しいタスクカードが作成されました！', { timeout: 1600 })
    router.push({ name: 'TaskApp' })
  } catch (error) {
    let message = 'タスクの作成に失敗しました。'
    if (axios.isAxiosError(error) && error.response) {
      if (typeof error.response.data.detail === 'string') {
        message = error.response.data.detail
        //エラー詳細が配列（複数バリデーションエラーなど）であれば、各メッセージをカンマ区切りで連結
      } else if (Array.isArray(error.response.data.detail)) {
        message = error.response.data.detail.map((d: { msg: any }) => d.msg).join(', ')
      }
    }
    toast.error(message, { timeout: 2000 })
  } finally {
    isLoading.value = false
  }
}

const cancel = () => {
  router.push({ name: 'TaskApp' })
}
onMounted(fetchDataForForm)
</script>

<style lang="scss" scoped>
h2 {
  margin-bottom: 1rem;
}
</style>
<!-- https://api.tsugawa.otani-shokai.org/tasks -->
