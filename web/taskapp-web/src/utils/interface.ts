export interface Base {
  id: number
  name: string
}

export interface Priority {
  id: number
  importance: string
}

export interface Category {
  id: number
  name: string
  active: boolean
}

export interface Status {
  id: number
  name: string
  active: boolean
}

export interface Staff {
  id: number
  code: string
  name: string
  active: boolean
}

export interface TaskWithCategory {
  id: number
  title: string
  category: Base
}

export interface TaskDetail {
  id: number
  name: string
  status: Status
  staff: Base
  priority: Priority
  start_date: string | null
  end_date: string | null
  active: boolean
}

export interface KanbanColumnData {
  id: number
  title: string
  active: boolean
  category: Category
  task_detail: TaskDetail[]
}
// export interface KanbanColumnData {
//   task_detail: TaskDetail[]
// }

export interface TaskGroup {
  task_id: number
  title: string
  category_name: string
  display_name: string
}

export interface Payload {
  detail_name: string
  status_id: number
  staff_id: number
  priority_id: number
  task_id?: number
  new_task_title?: string
  category_id?: number
  new_category_name?: string
  start_date?: string | null
  end_date?: string | null
}
