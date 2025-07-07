<template lang="pug">
div
  AddTaskBtn(@click="goToAddTaskPage")
  .loading(v-if="isLoading")
    p 読み込み中...
  .error(v-if="errorMessage") {{ errorMessage }}
  .api-message(v-if="apiMessage && !errorMessage" :class="{ 'success': isSuccessMessage, 'error': !isSuccessMessage }") {{ apiMessage }}
  .task-group-list-wrapper(v-if="!isLoading && !errorMessage")
    .task-group-list.flex.items-start
      TaskGroups(
        v-for="columnData in displayTaskGroups"
        :key="columnData.id"
        :group="columnData"
        @edit-task="handleEditTask"
        @delete-task="deleteTaskHandler"
      )
      //- TaskGroupにKanbanColumnDataのデータを渡す
  Modal(
    :is-visible="isEditModalVisible"
    :task-to-edit="taskToEdit"
    :TaskGroupList="taskGroupListForModal"
    :staff-list="staffList"
    :priority-list="priorityList"
    :all-task-groups="displayTaskGroups"
    @close="closeEditModal"
    @save-task="saveTaskChanges"
  )
  DeleteModal(
    :is-visible="isDeleteModalVisible"
    :task-title="taskTitleToDelete"
    @close="closeDeleteModal"
    @confirm-delete="confirmActualDelete"
  )
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AddTaskBtn from '@/components/AddTaskBtn.vue'
import TaskGroups from '@/components/TaskGroup.vue'
import { useRouter } from 'vue-router'
import Modal from '@/components/EditModal.vue'
import DeleteModal from '@/components/DeleteModal.vue'
import { useToast } from 'vue-toastification'
import { TASK_DETAIL_BASE_URL, STAFF_BASE_URL, PRIORITY_BASE_URL } from '@/utils/endpoints.ts'
import type {
  TaskDetail,
  KanbanColumnData,
  Base,
  Priority,
  TaskGroup,
  TaskWithCategory,
} from '@/utils/interface.ts'

// interface Staff {
//   //Base
//   id: number
//   name: string
// }

// interface Status {
//   id: number
//   name: string
//   active: boolean
// }
// interface Priority {
//   id: number
//   importance: string
// }

// interface TaskDetail {
//   id: number
//   name: string
//   status: Status
//   staff: Staff
//   priority: Priority // priorityオブジェクトを追加
//   start_date: string | null
//   end_date: string | null
//   active: boolean
// }

// interface TaskGroup {
//   task_id: number
//   title: string
//   category_name: string
//   display_name: string
// }

// interface TaskWithCategory {
//   id: number
//   title: string
//   category: { id: number; name: string }
// }

//状態管理
const isDeleting = ref<Record<number, boolean>>({})
const apiMessage = ref('')

const router = useRouter()
const toast = useToast()
const displayTaskGroups = ref<KanbanColumnData[]>([])
const staffList = ref<Base[]>([])
const priorityList = ref<Priority[]>([])
const taskGroupListForModal = ref<Array<TaskGroup>>([]) //リスト用
const isLoading = ref(false)
const errorMessage = ref('')
const isEditModalVisible = ref(false) //モーダルの表示・非表示
const taskToEdit = ref<(TaskDetail & { groupId?: number }) | null>(null)
const isDeleteModalVisible = ref(false) //削除モーダルの表示非表示
const taskIdToDelete = ref<number | null>(null)
const taskTitleToDelete = ref<string | null>(null)

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
      ]) //withのレスポンスとURLを追加
    // https://api.tsugawa.otani-shokai.org/tasks

    displayTaskGroups.value = tasksResponse.data
    // displayTaskGroupsはKanbanColumnDataと同じ構造
    console.log('---TaskGroupに渡すデータ---', displayTaskGroups.value)
    staffList.value = staffResponse.data
    priorityList.value = priorityResponse.data
    taskGroupListForModal.value = tasksWithCategoryResponse.data.map((task) => ({
      task_id: task.id,
      title: task.title,
      category_name: task.category.name,
      display_name: `${task.title}: ${task.category.name}`,
    }))
    console.log(taskGroupListForModal.value)
    console.log(staffList.value)
  } catch (error) {
    errorMessage.value = 'データの読み込みに失敗しました'
    toast.error(errorMessage.value, { timeout: 2000 })
  } finally {
    isLoading.value = false
  }
}
onMounted(fetchData)

//編集対象のタスク受取
const handleEditTask = (taskId: number) => {
  let foundTask: TaskDetail | undefined
  let foundGroupId: number | undefined

  for (const group of displayTaskGroups.value) {
    foundTask = group.task_detail.find((task) => task.id === taskId)
    if (foundTask) {
      foundGroupId = group.id // タスクが見つかったグループのIDを取得
      break // 見つかったらループを抜ける
    }
  }

  if (foundTask && foundGroupId !== undefined) {
    // 取得したタスク情報に、グループIDを追加してモーダルに渡す
    taskToEdit.value = { ...foundTask, groupId: foundGroupId }
    isEditModalVisible.value = true
  } else {
    toast.error('編集対象のタスクが見つかりませんでした。', { timeout: 2000 })
  }
}

const saveTaskChanges = async (updatedTaskData: any) => {
  const payload = {
    id: updatedTaskData.id,
    title: updatedTaskData.title,
    task_id: updatedTaskData.task_id, // フロントの'groupId'を'task_id'に合わせる
    status_id: updatedTaskData.status_id, // フロントの'status'を'status_id'に合わせる
    staff_id: updatedTaskData.staff_id,
    priority_id: updatedTaskData.priority_id,
    start_date: updatedTaskData.start_date,
    end_date: updatedTaskData.end_date,
  }
  try {
    // APIの更新エンドポイントはPUTを想定
    await axios.put(`${TASK_DETAIL_BASE_URL}/${updatedTaskData.id}`, payload)
    toast.success('タスクを更新しました！', { timeout: 1600 })
    closeEditModal()
    await fetchData() // 成功したら一覧を再取得
  } catch (error) {
    console.error('タスクの更新に失敗しました:', error)
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`更新に失敗しました: ${error.response.data.detail || 'サーバーエラー'}`, {
        timeout: 2000,
      })
    } else {
      toast.error('タスクの更新に失敗しました。', { timeout: 2000 })
    }
  }
}

const closeEditModal = () => {
  isEditModalVisible.value = false
  // editingTaskDetailId.value = null // IDをリセット
}
const goToAddTaskPage = () => {
  router.push('/taskapp/add')
}

//IDをもとに削除対象のタスクを探す
const deleteTaskHandler = (taskId: number) => {
  let foundTask: TaskDetail | undefined
  console.log(displayTaskGroups.value)
  // displayTaskGroups 配列内のすべてのグループをループ
  for (const group of displayTaskGroups.value) {
    // 各グループが持つ task_detail 配列の中から、IDが一致するタスクを探す
    const task = group.task_detail.find((t) => t.id === taskId)
    // タスクが見つかった場合
    if (task) {
      foundTask = task // 見つかったタスクを保存して
      console.log(foundTask)
      break // ループを終了
    }
  }
  // ループの結果、タスクが見つかっていれば
  if (foundTask) {
    // 削除確認モーダルを表示するために、IDとタスク名を設定
    taskIdToDelete.value = foundTask.id
    taskTitleToDelete.value = foundTask.name
    isDeleteModalVisible.value = true
  } else {
    // 万が一見つからなかった場合のために、エラーメッセージを表示
    toast.error('削除対象のタスクが見つかりませんでした。', { timeout: 2000 })
  }
}

//タスクの非アクティブ化(削除)
const confirmActualDelete = async () => {
  if (taskIdToDelete.value === null) return

  const currentTaskId = taskIdToDelete.value
  isDeleting.value[currentTaskId] = true
  apiMessage.value = ''
  errorMessage.value = ''

  try {
    await axios.patch(`${TASK_DETAIL_BASE_URL}/${currentTaskId}`)

    toast.success('タスクを削除しました。', { timeout: 1600 })

    // 画面を再読み込みして、リストからタスクが消えたことを反映
    await fetchData()
  } catch (error) {
    console.error('タスクの削除に失敗しました:', error)
    if (axios.isAxiosError(error) && error.response) {
      toast.error(`処理に失敗しました: ${error.response.data.detail || 'サーバーエラー'}`, {
        timeout: 2000,
      })
    } else {
      toast.error('タスクの削除に失敗しました。', { timeout: 2000 })
    }
  } finally {
    delete isDeleting.value[currentTaskId]
    closeDeleteModal()
  }
}

const closeDeleteModal = () => {
  isDeleteModalVisible.value = false
  taskIdToDelete.value = null
  taskTitleToDelete.value = null
}
</script>

<style lang="scss" scoped></style>
