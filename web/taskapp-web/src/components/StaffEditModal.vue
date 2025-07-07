<template lang="pug">
//- v-ifで表示を制御するモーダルの外枠
.fixed.inset-0.bg-black.bg-opacity-50.flex.justify-center.items-center.p-4(v-if="isVisible" @click.self="closeModal")
  //- モーダルの本体
  .bg-white.rounded-lg.shadow-xl.w-full.max-w-md(@click.stop)
    //- ヘッダー
    .bg-blue-600.text-white.flex.items-center.p-4.rounded-t-lg
      h3.flex-1.text-center.text-xl.font-semibold.mb-0 スタッフ情報を編集
      button.border-none.bg-blue-600(type="button" @click="closeModal")
        span.text-2xl(aria-hidden="true") &times;


    //- フォーム
    form.p-6(@submit.prevent="save")
      //- 職員コード入力欄
      .mb-6
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="edit-staff-code") 職員コード
        input#edit-staff-code.shadow-sm.border.border-gray-300.rounded.w-full.py-2.text-gray-700.outline-none(
          type="text"
          v-model.trim="editableStaff.code"
          required
          maxlength="6"
          pattern="^[0-9]{6}$"
        )
        p.text-xs.text-gray-500.mt-1 半角数字6桁で入力

      //- 氏名入力欄
      .mb-8
        label.block.text-gray-700.text-sm.font-bold.mb-2(for="edit-staff-name") 氏名
        input#edit-staff-name.shadow-sm.border.border-gray-300.rounded.w-full.py-2.text-gray-700.outline-none(
          type="text"
          v-model.trim="editableStaff.name"
          required
        )

      //- フッターのボタンエリア
      .flex.justify-center.border-t.pt-4.mt-4
        button.bg-gray-500.hover-bg-gray-700.text-white.font-bold.py-2.px-4.rounded.mr-4.border-none(
          type="button"
          @click="closeModal"
        ) キャンセル

        button.bg-blue-600.hover-bg-blue-700.text-white.font-bold.py-2.px-9.rounded.border-none(
          type="submit"
        ) 保存
</template>

<script setup lang="ts">
import { ref, watch, type PropType } from 'vue'
import type { Staff } from '@/utils/interface.ts'

// interface Staff {
//   id: number
//   code: string
//   name: string
// }

const props = defineProps({
  // モーダルの表示状態
  isVisible: {
    type: Boolean,
    required: true,
  },
  // 編集対象のスタッフ情報
  staffToEdit: {
    type: Object as PropType<Staff | null>,
    default: null,
  },
})

const emit = defineEmits<{
  (e: 'close'): void // モーダルを閉じるイベント
  (e: 'save', staffData: Staff): void // 更新されたスタッフ情報を渡す
}>()

const editableStaff = ref<Staff>({ id: 0, code: '', name: '', active: true })

// props.staffToEditが変更されたら、モーダル内のフォームに値をコピーする
watch(
  () => props.staffToEdit,
  (newStaff) => {
    if (newStaff) {
      editableStaff.value = { ...newStaff }
    } else {
      // 対象がなければフォームをリセット
      editableStaff.value = { id: 0, code: '', name: '', active: true }
    }
  },
  {
    deep: true,
    immediate: true, // 初期読み込み時も実行する
  },
)

const closeModal = () => {
  emit('close')
}

const save = () => {
  emit('save', editableStaff.value)
}
</script>

<style lang="scss" scoped>
// .close-button {
//   item
// }
</style>
