<template lang="pug">
.task-card.bg-gray-2.rounded-md.hover-shadow-lg.font-semibold.text-size-4.mb-3.w-350
  .class-1.flex
    span.status-badge.text-white.px-3.rounded-full.ml-4.mt-3.w-13.text-center(
      v-if="props.task.status"
      :class="{ \
        'bg-gray-500': props.task.status.id === 1,  /*ID 1 未着手*/ \
        'bg-blue-500': props.task.status.id === 2,  /*ID 2 進行中*/ \
        'bg-green-500': props.task.status.id === 3   /*ID 3 完了*/ \
      }"
    ) {{ props.task.status.name }}

    .priority-badge.mt-3.w-40
      span.priority-badge.text-white.px-3.py-1.mr-5.rounded.text-3.font-medium.text-center(
        v-if="props.task.priority"
      :class="{ \
        'bg-red-600': props.task.priority.id === 1,      /* 重要度高、緊急度高 */ \
        'bg-orange-500': props.task.priority.id === 2,   /* 重要度高、緊急度低 */ \
        'bg-yellow-500': props.task.priority.id === 3,   /* 重要度低、緊急度高 */ \
        'bg-sky-500': props.task.priority.id === 4,      /* 重要度低、緊急度低 */ \
        'bg-gray-400': props.task.priority.id === 5      /* 重要度なし */ \
      }"
    ) {{ props.task.priority.importance }}

    .staff-info.flex.items-center.text-size-4.text-gray-600.mr-5.mt-3(v-if="props.task.staff")
      svg.w-4.h-4.mr-1(xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor")
        path(d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z")
      span.w-45 {{ props.task.staff.name }}

    .calender-info.flex.items-center.text-size-4.text-gray-600.mt-3
      svg.w-4.h-4.mr-1(xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor")
        path(fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd")
      div
        span(v-if="props.task.start_date") {{ props.task.start_date }}  ～
        span(v-if="props.task.start_date && props.task.end_date")
        span(v-if="props.task.end_date") {{ props.task.end_date }}

  .task-card-header.text-size-5.justify-between.mt-5.ml-4.flex
    h3.mr-6.mb-4 {{ props.task.name }}

    .task-actions.flex
      button.border-none.text-sm.bg-yellow-500.hover-bg-yellow-600.text-white.font-medium.py-1.text-center.w-20.rounded-md(
        @click="onEditClick"
      ) 編集
      button.border-none.text-sm.bg-red-500.hover-bg-red-600.text-white.font-medium.py-1.text-center.w-20.rounded-md.mr-4(
        @click="onDeleteClick"
      ) 削除
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
import type { TaskDetail } from '@/utils/interface.ts'

// interface Staff {
//   id: number
//   name: string
// }

// interface Priority {
//   id: number
//   importance: string
// }

//親から受け取りたいデータ型
// interface TaskDetail {
//   id: number
//   name: string
//   status: string
//   staff: Staff
//   priority: Priority
//   start_date: string | null
//   end_date: string | null
//   active: boolean
// }

// TaskGroupからTaskDetailもらう
const props = defineProps({
  task: {
    type: Object as PropType<TaskDetail>,
    required: true,
  },
})
const emit = defineEmits<{
  (e: 'edit-task', id: number): void
  (e: 'delete-task', id: number): void
}>()

const onEditClick = () => {
  emit('edit-task', props.task.id)
}

const onDeleteClick = () => {
  emit('delete-task', props.task.id)
}
</script>

<style lang="scss" scoped>
.status-badge {
  margin-right: 1rem;
  white-space: nowrap;
}
.task-actions {
  // margin-top: 2rem;
  margin-bottom: 1rem;
  margin-right: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 2em;
}
</style>
