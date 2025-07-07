<template lang="pug">
.calendar-container.p-4.md-p-8
  //- カレンダーヘッダー：年月表示とナビゲーション
  .calendar-header.flex.justify-between.items-center.mb-4
    button.nav-button.w-28.flex-shrink-0.justify-center(@click="prevMonth") &lt; 前月
    h2.text-2xl.font-bold.flex-grow.text-center {{ currentYear }}年 {{ currentMonth + 1 }}月
    button.nav-button.w-28.flex-shrink-0.justify-center(@click="nextMonth") 次月 &gt;
  //- &lt; &gt; で< > を表す
  .loading(v-if="isLoading")
    p データの読み込み中...
  .error(v-else-if="errorMessage")
    p.text-red-500 {{ errorMessage }}

  //- カレンダー本体
  .calendar-grid(v-else)
    //- 曜日ヘッダー
    .day-of-week(v-for="day in weekDays" :key="day") {{ day }}

    //- 日付セル goToDateDetail(その日のtask_detailをまとめたぺーじへ)
    .date-cell(
      v-for="(day, index) in calendarDays"
      :key="index"
      :class="{ 'is-not-current-month': !day.isCurrentMonth,'has-tasks': day.tasks.length > 0 }"
      @click="goToTaskDetail(day)"
    )
      .date-number {{ day.date }}
      .tasks-wrapper
        //- 各日付に紐づくタスクを表示
        //-ラッパーで括り、priorityのidによってbgの色を変える
        .task-item(
          v-for="task in day.tasks"
          :key="task.id"
          :class="priorityClass(task.priority.id)"
        )
          span.status {{ task.status.name }}:&nbsp;
          span.staff {{ task.staff.name }}
//- &nbsp　これで空白をいれるらしい
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { TASK_DETAIL_BASE_URL } from '@/utils/endpoints'
import { useRouter } from 'vue-router'
import type { TaskDetail, KanbanColumnData } from '@/utils/interface'

// interface Status {//Base
//   id: number
//   name: string
// }
// interface Staff {//Base
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
// }
// interface KanbanColumnData {
//   task_detail: TaskDetail[]
// }

const router = useRouter()
const isLoading = ref(true)
const errorMessage = ref('')
const currentDate = ref(new Date()) // 現在表示している年月を管理
const allTasks = ref<TaskDetail[]>([]) // APIから取得した全てのタスク
const calculationDays = ref<number>(0)
//曜日ヘッダー
const weekDays = ['日', '月', '火', '水', '木', '金', '土']

//データ取得
const fetchAllTasks = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const response = await axios.get<KanbanColumnData[]>(TASK_DETAIL_BASE_URL)
    // 全ての列からtask_detailを抽出し、一つの配列にまとめる
    allTasks.value = response.data.flatMap((column) => column.task_detail)
  } catch (e) {
    errorMessage.value = 'タスクデータの取得に失敗しました。'
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

//computedを使った算出プロパティ
const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())

// カレンダーに表示する日付とタスクのデータを生成するメインロジック
const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value

  // javaのDateオブジェクトを使った計算しているらしい
  const firstDayOfMonth = new Date(year, month, 1).getDay() // 月の初日の曜日 (0=日, 1=月, ...)
  // const lastDaytOfMonth = new Date()
  const daysInMonth = new Date(year, month + 1, 0).getDate() // その月の日数

  const days = []

  // 月の初日までの空白セルを追加
  for (let i = 0; i < firstDayOfMonth; i++) {
    days.push({ date: '', isCurrentMonth: false, tasks: [], dayDate: null })
  }

  // その月の日付を1日から順番に処理するループ
  for (let i = 1; i <= daysInMonth; i++) {
    // 「YYYY-MM-DD」形式の文字列を作成.2025年7月3日の場合、「2025-07-03」という文字列を作る
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    // 全タスクから、この日付に開始するタスク（start_dateと同じ）をフィルタリング
    const tasksForDay = allTasks.value.filter((task) => task.start_date === dateStr)

    // 日付（i）とフィルターをかけたtasksForDayリストをセット
    days.push({
      date: i,
      isCurrentMonth: true,
      tasks: tasksForDay,
      dayDate: dateStr,
    })
  }

  // 31日以降の日曜日までの空欄補充
  // daysにその月の配列の長さが入っている
  // ７で割ったあまり分空の配列をいれる
  const remainingDays = () => {
    calculationDays.value = 7 - (days.length % 7)
    if (calculationDays.value === 7) {
      calculationDays.value = 0
    }
    return calculationDays.value
  }
  remainingDays()
  for (let i = 0; i < calculationDays.value; i++) {
    days.push({ date: '', isCurrentMonth: false, tasks: [] })
  }
  console.log(days)
  return days
})

//カレンダーのグリットを押したときの動作
const goToTaskDetail = (day: { tasks: []; isCurrentMonth: boolean; dayDate: string | null }) => {
  // タスクが存在し、かつ当月の日付である場合のみ遷移
  if (day.tasks.length > 0 && day.isCurrentMonth && day.dayDate) {
    router.push({ name: 'TaskDetail', params: { dateString: day.dayDate } })
    // dataStringにdayDateの文字列いれる
  }
}

const prevMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}
const nextMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

// 優先度IDに応じてCSSクラスを返す関数
const priorityClass = (priorityId: number) => {
  switch (priorityId) {
    case 1:
      return 'priority-high'
    case 2:
      return 'priority-medium'
    case 3:
      return 'priority-low'
    case 4:
      return 'priority-very-low'
    case 5:
      return 'priority-none'
  }
}
onMounted(fetchAllTasks)
</script>

<style lang="scss" scoped>
.calendar-container {
  width: 150vh;
  margin: 0 auto;
  height: 80vh;
}

.nav-button {
  background-color: #3b82f6;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  &:hover {
    background-color: #2563eb;
  }
}

.calendar-grid {
  display: grid;
  // グリッドコンテナを宣言
  grid-template-columns: repeat(7, 1fr); //7個で区切る
  // repeat(7, 1fr)は利用可能な幅を均等に7分割した列を7つ作成する
  border-top: 2px solid #e5e7eb;
  border-left: 2px solid #e5e7eb;
}

.day-of-week,
.date-cell {
  text-align: center;
  padding: 8px;
  border-right: 2px solid #e5e7eb;
  border-bottom: 2px solid #e5e7eb;
  // max-width: 8rem;
  // min-width: 8rem;
}

.day-of-week {
  font-weight: bold;
  background-color: #f3f4f6;
}

.date-cell {
  min-height: 120px;
  text-align: left;
  &.is-not-current-month {
    background-color: #f9fafb;
    color: #d1d5db;
  }
}

.date-number {
  font-weight: 600;
}

.tasks-wrapper {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-item {
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.priority-high {
  background-color: red;
} /* red-600 dc2626*/
.priority-medium {
  background-color: orange;
} /* orange-500 f97316*/
.priority-low {
  background-color: rgb(224, 224, 73);
} /* yellow-500 f59e0b*/
.priority-very-low {
  background-color: skyblue;
} /* sky-500 0ea5e9*/
.priority-none {
  background-color: gray;
} /* gray-400 9ca3af*/
</style>
