<template lang="pug">
  .task-group(
    class="bg-yellow-200 text-center p-4 rounded-md flex-shrink-0 w-70 ml-10"
  )
    .column-header.flex.justify-between.items-center.mb-4
      h2.text-lg.font-bold.mb-2.ml-2.text-gray-800.text-center {{ props.group.title }}
      span.category-badge.text-size-4.font-medium.px-4.py-2.rounded-full(
        v-if="props.group.category"
        class="bg-blue-100 text-blue-800"
      ) {{ props.group.category.name }}

    .task-cards.space-y-3
      TaskCard(
        v-for="detailItem in props.group.task_detail"
        :key="detailItem.id"
        :task="detailItem"
        @edit-task="onEditTask"
        @delete-task="onDeleteTask"
      )
      //- props.group.task_detail　もとの変数

      //-タスクカードにはtask_detailを渡す　TaskDetailと同じ型
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import TaskCard from '@/components/TaskCard.vue'
import { computed } from 'vue'
import type { KanbanColumnData } from '@/utils/interface.ts'

// interface Category {
//   id: number
//   name: string
//   active: boolean
// }
// interface Status {
//   id: number
//   name: string
//   active: boolean
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
//   status: Status
//   staff: Staff
//   priority: Priority
//   start_date: string | null
//   end_date: string | null
//   active: boolean
// }

// interface KanbanColumnData {
//   id: number
//   title: string
//   active: boolean
//   category: Category
//   task_detail: TaskDetail[]
// }

const props = defineProps({
  group: {
    type: Object as PropType<KanbanColumnData>,
    required: true,
  },
})

//ソート
// const sortedTaskDetails = computed(() => {
//   // 元の配列をコピーを作成してからソートする
//   return [...props.group.task_detail].sort((a, b) => {
//     return a.priority.id - b.priority.id
//   })
// })

const emit = defineEmits<{
  (e: 'edit-task', id: number): void
  (e: 'delete-task', id: number): void
}>()

const onEditTask = (taskId: number) => {
  emit('edit-task', taskId)
}
const onDeleteTask = (taskId: number) => {
  emit('delete-task', taskId)
}
</script>

<style lang="scss" scoped></style>
