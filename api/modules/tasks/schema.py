from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

from modules.category.schema import CategorySchema
from modules.status.schema import StatusSchema


class TaskBase(BaseModel):
    title: str = Field(None, json_schema_extra={"example": "クリーニングを取りに行く"})


class TasksResponse(BaseModel):  # tasksだけ
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    active: bool
    category: CategorySchema


class CategorySchima(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    active: bool


class PriorityDetailSchema(BaseModel):  # 優先度
    model_config = ConfigDict(from_attributes=True)

    id: int
    importance: str


class StaffDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    active: bool


class TaskDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    staff: StaffDetailSchema
    status: StatusSchema
    priority: PriorityDetailSchema
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: bool


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    active: bool
    category: CategorySchema
    task_detail: List[TaskDetailSchema]


class CompositeTaskCreate(BaseModel):  # id or name のリクエストとvalidation
    detail_name: str = Field(..., description="作成するタスクカードのタイトル")
    status_id: Optional[int] = Field(default=1)
    task_id: Optional[int] = Field(default=None)
    new_task_title: Optional[str] = Field(default=None)
    staff_id: int = Field(..., description="担当するスタッフのID")
    priority_id: int = Field(..., description="タスクの優先度ID")
    start_date: Optional[date] = Field(default=None, description="タスクの開始日")
    end_date: Optional[date] = Field(default=None, description="タスクの終了日")
    category_id: Optional[int] = Field(default=None)
    new_category_name: Optional[str] = Field(default=None)
    # ドロップダウンから指定した場合はid(int),新規の場合はname(str)が来る予定


# TaskCreateをTaskUpdateに変更
class TaskUpdate(TaskBase):
    id: int
    title: Optional[str]
    # category_id: int
    task_id: Optional[int]
    staff_id: Optional[int] = Field(default=None)
    status_id: Optional[int]
    priority_id: Optional[int]
    start_date: Optional[date] = Field(default=None, description="変更後の開始日")
    end_date: Optional[date] = Field(default=None, description="変更後の終了日")


# TaskCreateResponseをTaskUpdateResponseに変更
class TaskUpdateResponse(TaskUpdate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    active: bool
    category: CategorySchema
    task_detail: List[TaskDetailSchema] = []


class DeleteTaskResponse(BaseModel):
    id: int
