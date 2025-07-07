import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import LoginScreen from '../pages/LoginScreen.vue'
import AttendanceSystem from '../pages/AttendanceSystem.vue'
import KanbanBoard from '@/pages/KanbanBoard.vue'
import AddTask from '@/pages/AddTask.vue'
import AddStaff from '@/pages/AddStaff.vue'
import StaffList from '@/pages/StaffList.vue'
import Calendar from '@/pages/Calendar.vue'
import TaskList from '@/pages/TaskList.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/taskapp',
  },
  {
    path: '/taskapp',
    name: 'TaskApp',
    component: KanbanBoard,
  },
  {
    path: '/taskapp/add',
    name: 'AddTask',
    component: AddTask,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginScreen,
  },
  {
    path: '/attendance',
    name: 'Attendance',
    component: AttendanceSystem,
  },
  {
    path: '/staffs',
    name: 'StaffList',
    component: StaffList,
  },
  {
    path: '/staffs/add',
    name: 'AddStaff',
    component: AddStaff,
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
  },
  {
    // :dateString の部分が動的なパラメータになる(例: /date/2025-07-03)
    // props: true を設定すると、URLのパラメータをコンポーネントのpropsとして受け取れる
    path: '/calendar/tasklist-date/:dateString',
    name: 'TaskDetail',
    component: TaskList,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
