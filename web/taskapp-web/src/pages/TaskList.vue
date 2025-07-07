<template lang="pug">
.date-detail-container.md-p-8

  .flex.items-center.mb-5
    button.back-button(@click="goBack") &lt; カレンダーに戻る
    h1.text-2xl.font-bold.ml-10 {{ dateString }} のタスク

  .loading(v-if="isLoading")
    p データの読み込み中...
  .error(v-else-if="errorMessage")
    p.text-red-500 {{ errorMessage }}

  .no-tasks(v-else-if="tasksForDate.length === 0")
    p この日付に開始するタスクはありません。


  .task-list-wrapper.space-y-4(v-else)
    TaskCard(
      v-for="task in tasksForDate"
      :key="task.id"
      :task="task"
      @edit-task="openEditModal(task.id)"
      @delete-task="openDeleteModal(task.id)"
    )

  EditModal(
    :is-visible="editModal.isVisible"
    :task-to-edit="editModal.taskToEdit"
    :TaskGroupList="taskGroupListForModal"
    :staff-list="staffList"
    :priority-list="priorityList"
    :is-saving="editModal.isSaving"
    @close="closeEditModal"
    @save-task="saveTaskChanges"
  )
  DeleteModal(
    :is-visible="deleteModal.isVisible"
    :task-title="deleteModal.taskToDelete ? deleteModal.taskToDelete.name : null"
    @close="closeDeleteModal"
    @confirm-delete="confirmActualDelete"
  )
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { TASK_DETAIL_BASE_URL, STAFF_BASE_URL, PRIORITY_BASE_URL } from '@/utils/endpoints'
import TaskCard from '@/components/TaskCardForTaskList.vue'
import EditModal from '@/components/EditModal.vue'
import DeleteModal from '@/components/DeleteModal.vue'
import type {
  Base,
  Priority,
  TaskDetail,
  TaskWithCategory,
  KanbanColumnData,
} from '@/utils/interface.ts'

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
// interface TaskDetail {
//   id: number
//   name: string
//   status: Base
//   staff: Base
//   priority: Priority
//   start_date: string | null
//   end_date: string | null
//   active: boolean
// }
// interface TaskWithCategory {
//   id: number
//   title: string
//   category: { id: number; name: string }
// }
// interface KanbanColumnData {
//   id: number
//   title: string
//   category: Base
//   task_detail?: TaskDetail[]
// }

interface ModalTaskGroup {
  task_id: number
  display_name: string
}
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

const props = defineProps<{ dateString: string }>()

const router = useRouter()
const toast = useToast()
const isLoading = ref(true)
const errorMessage = ref('')
const allKanbanData = ref<KanbanColumnData[]>([]) // APIからの生のネストされたデータを保持

// モーダル用の選択肢リスト
const staffList = ref<Base[]>([])
const priorityList = ref<Priority[]>([])
const taskGroupListForModal = ref<ModalTaskGroup[]>([])

// 編集モーダルの状態
const editModal = reactive({
  isVisible: false,
  isSaving: false,
  taskToEdit: null as (TaskDetail & { groupId: number }) | null,
})

// 削除モーダルの状態
const deleteModal = reactive({
  isVisible: false,
  taskToDelete: null as TaskDetail | null,
})

// 表示用のタスクリストを算出
const tasksForDate = computed(() => {
  const allTaskDetails = allKanbanData.value.flatMap((column) => column.task_detail || [])
  return allTaskDetails.filter((task) => task.start_date === props.dateString)
})

const fetchData = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const [tasksResponse, staffResponse, tasksWithCategoryResponse, priorityResponse] =
      await Promise.all([
        axios.get<KanbanColumnData[]>(TASK_DETAIL_BASE_URL),
        axios.get<Base[]>(STAFF_BASE_URL),
        axios.get<TaskWithCategory[]>(`${TASK_DETAIL_BASE_URL}/with_category`),
        axios.get<Priority[]>(PRIORITY_BASE_URL),
      ])

    allKanbanData.value = tasksResponse.data // 全てのネストされたデータを保存
    staffList.value = staffResponse.data
    priorityList.value = priorityResponse.data
    taskGroupListForModal.value = tasksWithCategoryResponse.data.map((task) => ({
      task_id: task.id,
      display_name: `${task.title} : ${task.category.name}`,
    }))
  } catch (e) {
    errorMessage.value = 'データの取得に失敗しました。'
  } finally {
    isLoading.value = false
  }
}
onMounted(fetchData)

const goBack = () => {
  router.push('/calendar')
}

const openEditModal = (taskId: number) => {
  let foundTask: TaskDetail | undefined
  let foundGroupId: number | undefined
  // ネストされた元のデータ(allKanbanData)をループして、親のIDを探す
  for (const group of allKanbanData.value) {
    foundTask = (group.task_detail || []).find((task) => task.id === taskId)
    if (foundTask) {
      foundGroupId = group.id // 親のIDが見つかった！
      break
    }
  }
  if (foundTask && foundGroupId !== undefined) {
    editModal.taskToEdit = { ...foundTask, groupId: foundGroupId }
    editModal.isVisible = true
  } else {
    toast.error('編集対象のタスクが見つかりませんでした。', { timeout: 2000 })
  }
}
const closeEditModal = () => {
  editModal.isVisible = false
  editModal.taskToEdit = null
}

const openDeleteModal = (taskId: number) => {
  const allTaskDetails = allKanbanData.value.flatMap((group) => group.task_detail || [])
  const foundTask = allTaskDetails.find((task) => task.id === taskId)
  if (foundTask) {
    deleteModal.taskToDelete = foundTask
    deleteModal.isVisible = true
  } else {
    toast.error('削除対象のタスクが見つかりませんでした。', { timeout: 2000 })
  }
}
const closeDeleteModal = () => {
  deleteModal.isVisible = false
  deleteModal.taskToDelete = null
}

const saveTaskChanges = async (updatedTaskData: FormState) => {
  editModal.isSaving = true
  try {
    await axios.put(`${TASK_DETAIL_BASE_URL}/${updatedTaskData.id}`, updatedTaskData)
    toast.success('タスクを更新しました！', { timeout: 1600 })
    closeEditModal()
    await fetchData()
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`更新に失敗しました: ${error.response.data.detail || 'サーバーエラー'}`, {
        timeout: 2000,
      })
    } else {
      toast.error('タスクの更新中にエラーが発生しました。', { timeout: 2000 })
    }
  } finally {
    editModal.isSaving = false
  }
}

const confirmActualDelete = async () => {
  if (!deleteModal.taskToDelete) return
  try {
    await axios.patch(`${TASK_DETAIL_BASE_URL}/${deleteModal.taskToDelete.id}`)
    toast.success(`${deleteModal.taskToDelete.name} 削除しました。`, { timeout: 1600 })
    closeDeleteModal()
    await fetchData()
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`処理に失敗しました: ${error.response.data.detail || 'サーバーエラー'}`),
        { timeout: 2000 }
    } else {
      toast.error('削除処理中にエラーが発生しました。', { timeout: 2000 })
    }
  }
}
</script>

<style lang="scss" scoped>
.date-detail-container {
  max-width: 150vh;
  margin: 0 auto;
}
.back-button {
  background-color: #f3f4f6;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  &:hover {
    background-color: #e5e7eb;
  }
}
</style>
