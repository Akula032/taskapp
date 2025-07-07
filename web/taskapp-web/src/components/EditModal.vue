<template lang="pug">
.fixed.inset-0.bg-black.bg-opacity-50.flex.justify-center.items-center.p-4(v-if="isVisible" @click.self="closeModal" )
  .bg-white.rounded-lg.shadow-xl.w-full.max-w-md(@click.stop)
    .bg-blue-600.text-white.flex.justify-between.items-center.p-4.rounded-t-lg
      h3.flex-1.text-center.text-xl.font-semibold.ml-0 タスクを編集
      button.border-none.bg-blue-600(type="button" @click="closeModal")
        span.text-2xl(aria-hidden="true") &times;

    form.p-6(@submit.prevent="submitEdit")
      .mb-5
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="edit-task-title") タスクタイトル
        input#edit-task-title.shadow-sm.border.border-gray-300.rounded.w-full.py-2.text-gray-700.outline-none(
          type="text"
          v-model.trim="formState.title"
          required
        )
      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="category-select") タスクグループ
        select#category-select.w-full.p-2.rounded.text-gray-700.text-sm.font-medium(
          v-model="formState.task_id"
          required
        )
          option(disabled :value="0") グループを選択してください
          option(
            v-for="item in props.TaskGroupList"
            :key="item.task_id"
            :value="item.task_id"
          ) {{ item.display_name }}

      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="staff-select-edit") 担当スタッフ
        select#staff-select-edit.w-full.p-2.rounded.border.border-gray-300(v-model="formState.staff_id" required)
          option(:value="null" disabled) スタッフを選択してください
          option(v-for="staff in props.staffList" :key="staff.id" :value="staff.id") {{ staff.name }}

      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="priority-select-edit") 優先度
        select#priority-select-edit.w-full.p-2.rounded.text-gray-700.text-sm.font-medium(
          v-model="formState.priority_id"
          required
        )
          option(disabled :value="null") 優先度を選択してください
          option(
            v-for="priority in props.priorityList"
            :key="priority.id"
            :value="priority.id"
          ) {{ priority.importance }}

      .flex.space-x-4.mb-6
        .start-day.mr-5
          label.block.text-gray-700.text-sm.font-bold.mb-2(for="start-date") 開始日（任意）
          input#start-date.w-full.p-2.rounded.border.border-gray-300(
            type="date"
            v-model="formState.start_date"
          )
        .end-day
          label.block.text-gray-700.text-sm.font-bold.mb-2(for="end-date") 終了日（任意）
          input#end-date.w-full.p-2.rounded.border.border-gray-300(
            type="date"
            v-model="formState.end_date"
          )

      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-3 ステータス
        .flex.justify-center.space-x-8
          label.flex.items-center.cursor-pointer(v-for="status in statusList" :key="status.id" :for="'status-' + status.id")
            input(type="radio" name="task-status" v-model="formState.status_id" :id="'status-' + status.id" :value="status.id" class="h-5 w-5")
            span.ml-2.text-gray-800 {{ status.name }}

      .flex.justify-center.pt-4.mt-6
        button.border-none.bg-gray-500.hover-bg-gray-700.text-white.font-semibold.py-2.px-4.rounded-md.mr-10(type="button" @click="closeModal") キャンセル
        button.border-none.bg-blue-600.hover-bg-blue-700.text-white.font-semibold.py-2.px-9.rounded-md(type="submit" :disabled="isSaving" :class="{ 'opacity-75 cursor-not-allowed': isSaving }") {{ isSaving ? '更新中...' : '更新' }}
</template>

<script setup lang="ts">
import { ref, reactive, watch, type PropType } from 'vue'
import { useToast } from 'vue-toastification'
import type { Base, Priority } from '@/utils/interface.ts'

// interface Status {
//   id: number
//   name: string
// }
// interface Staff {
//   id: number
//   name: string
// }
// interface Priority {
//   id: number
//   importance: string
// }
interface TaskGroup {
  task_id: number
  display_name: string
}
// 親から渡されるタスク詳細の型
interface TaskToEdit {
  id: number
  name: string
  status: Base
  staff: Base
  priority: Priority
  start_date: string | null
  end_date: string | null
  groupId: number
}
// フォームの状態と、親に通知するデータの型
interface FormState {
  id: number
  title: string
  task_id: number
  status_id: number
  staff_id: number | null
  priority_id: number | null
  start_date: string | null
  end_date: string | null
}

const props = defineProps({
  isVisible: { type: Boolean, required: true },
  taskToEdit: { type: Object as PropType<TaskToEdit | null>, default: null }, //モーダル初期値
  TaskGroupList: { type: Array as PropType<TaskGroup[]>, required: true },
  staffList: { type: Array as PropType<Base[]>, required: true },
  priorityList: { type: Array as PropType<Priority[]>, required: true },
  isSaving: { type: Boolean, default: false },
})

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save-task', updatedTaskData: FormState): void
}>()

const toast = useToast()

// フォームの初期状態を定義
const initialFormState = (): FormState => ({
  id: 0,
  title: '',
  task_id: 0,
  status_id: 1,
  staff_id: null,
  priority_id: null,
  start_date: null,
  end_date: null,
})
// フォームの状態を管理するリアクティブな変数
const formState = reactive<FormState>(initialFormState())
// モーダルが開かれた時の初期状態を保持するための変数
const originalState = ref<string>('')

const statusList = ref<Base[]>([
  { id: 1, name: '未着手' },
  { id: 2, name: '進行中' },
  { id: 3, name: '完了' },
])

watch(
  () => props.taskToEdit,
  (newTask) => {
    // 編集対象のタスク(newTask)に中身がある場合
    if (newTask && newTask.id) {
      // 編集対象が渡されたら、その情報でフォームの状態を更新
      formState.id = newTask.id
      formState.title = newTask.name
      formState.task_id = newTask.groupId
      formState.status_id = newTask.status.id
      formState.staff_id = newTask.staff?.id ?? null
      formState.priority_id = newTask.priority?.id ?? null
      formState.start_date = newTask.start_date
      formState.end_date = newTask.end_date
      // 変更チェック用に、開いた時点の状態をJSON文字列として保存
      originalState.value = JSON.stringify(formState)
    } else {
      // モーダルが閉じられたらフォームをリセット
      Object.assign(formState, initialFormState())
    }
  },
  { deep: true, immediate: true }, // オブジェクトの変更を検知するために重要
)

const submitEdit = () => {
  // バリデーション
  if (
    !formState.title.trim() ||
    !formState.task_id ||
    !formState.status_id ||
    !formState.staff_id ||
    !formState.priority_id
  ) {
    toast.error('全ての項目を入力または選択してください。', { timeout: 2000 })
    return
  }
  //日付が空白文字だったらnullに変換
  const payloadToSend = { ...formState }
  if (payloadToSend.start_date === '') {
    payloadToSend.start_date = null
  }
  if (payloadToSend.end_date === '') {
    payloadToSend.end_date = null
  }

  // 変更チェック formStateからpayloadToSendに変更
  if (originalState.value === JSON.stringify(payloadToSend)) {
    toast.info('変更内容がありません。', { timeout: 1600 })

    return
  }
  // 現在のフォームの状態をそのまま親に通知する
  emit('save-task', { ...payloadToSend })
}

const closeModal = () => {
  emit('close')
}
</script>
