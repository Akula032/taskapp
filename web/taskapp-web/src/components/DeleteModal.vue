<template lang="pug">
.modal-overlay.fixed.inset-0.bg-black.bg-opacity-60.flex.justify-center.items-center.p-4(v-if="isVisible" @click.self="closeModal")
  .modal-box(@click.stop)
    .modal-header
      h1.font-semibold.text-gray-800.text-center 確認
      p.text-gray-700.text-center(v-if="taskTitle") 「{{ taskTitle }}」
      p.text-center を削除しますか？
    p.caution.text-sm.m-4.text-center.text-red-600 この操作は元に戻せません。
    .actions.pt-4.btn-flex
      button.border-none.bg-red-6.text-white.font-semibold.py-2.text-center.w-32.rounded-md(
        type="button"
        @click="confirmDelete"
      ) 削除します
      button.border-none.bg-gray.text-black.font-semibold.py-2.text-center.w-32.rounded-md(
        type="button"
        @click="closeModal"
      ) キャンセル
</template>

<script setup lang="ts">
import type { PropType } from 'vue'
const props = defineProps({
  isVisible: {
    type: Boolean,
    required: true,
  },
  taskTitle: {
    type: String as PropType<string | null>,
    default: null,
  },
})

const emit = defineEmits<{
  (e: 'confirm-delete'): void
  (e: 'close'): void
}>()

const confirmDelete = () => {
  emit('confirm-delete')
}

const closeModal = () => {
  emit('close')
}
</script>

<style lang="scss" scoped>
.modal-box {
  background: white;
  border-radius: 5px;
  width: 500px;
}
h1 {
  background-color: aqua;
  margin-bottom: 1rem;
  padding: 1rem 0;
  font-size: x-large;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.btn-flex {
  display: flex;
  justify-content: space-evenly;
  margin-bottom: 1rem;
}
</style>
