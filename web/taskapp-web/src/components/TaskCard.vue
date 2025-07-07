<template lang="pug">
.task-card.bg-white.p-2.rounded-md.hover-shadow-lg.font-semibold.text-size-4.mb-3
  .flex.justify-between.items-center
    span.status-badge.text-white.px-3.rounded-full(
      v-if="props.task.status"
      :class="{ \
        'bg-gray-500': props.task.status.id === 1,  /*ID 1 未着手*/ \
        'bg-blue-500': props.task.status.id === 2,  /*ID 2 進行中*/ \
        'bg-green-500': props.task.status.id === 3   /*ID 3 完了*/ \
      }"
    ) {{ props.task.status.name }}

    .staff-info.flex.items-center.text-sm.text-gray-600.mr-3(v-if="props.task.staff")
      svg.w-4.h-4.mr-1(xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor")
        path(d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z")
      //- スタッフの名前
      span {{ props.task.staff.name }}
      //- Gemin先生のユーザーアイコン (インラインSVG)

  .priority-badge.mt-2
    span.priority-badge.text-white.px-2.py-1.rounded.text-xs.font-medium(
      v-if="props.task.priority"
    :class="{ \
      'bg-red-600': props.task.priority.id === 1,      /* 重要度高、緊急度高 */ \
      'bg-orange-500': props.task.priority.id === 2,   /* 重要度高、緊急度低 */ \
      'bg-yellow-500': props.task.priority.id === 3,   /* 重要度低、緊急度高 */ \
      'bg-sky-500': props.task.priority.id === 4,      /* 重要度低、緊急度低 */ \
      'bg-gray-400': props.task.priority.id === 5      /* 重要度なし */ \
    }"
  ) {{ props.task.priority.importance }}

  .task-card-header.justify-between.items-start.mt-4
    h3 {{ props.task.name }}

  .date-section.mt-3.text-xs.text-gray-500.flex.items-center(v-if="props.task.start_date || props.task.end_date")
    //- カレンダーアイコン (インラインSVG)
    svg.w-4.h-4.mr-1.flex-shrink-0(xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor")
      path(fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd")
    //- 日付表示
    div
      span(v-if="props.task.start_date") {{ props.task.start_date }}
      span(v-if="props.task.start_date && props.task.end_date")  ～
      span(v-if="props.task.end_date") {{ props.task.end_date }}

  .task-actions
    button.border-none.text-sm.bg-yellow-500.hover-bg-yellow-600.text-white.font-medium.py-1.text-center.w-20.rounded-md(
      @click="onEditClick"
    ) 編集
    button.border-none.text-sm.bg-red-500.hover-bg-red-600.text-white.font-medium.py-1.text-center.w-20.rounded-md(
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
//   //優先度
//   id: number
//   importance: string
// }

//親から受け取りたいデータ型
// interface TaskDetail {
//   id: number
//   name: string
//   status: string
//   staff: Staff
//   priority: Priority //優先度
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
  margin-top: 2rem;
  margin-bottom: 0.5rem;
  margin-right: 0.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1em;
}
</style>
