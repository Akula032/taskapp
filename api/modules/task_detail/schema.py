from pydantic import BaseModel
from typing import Optional


class TaskDetailBase(BaseModel):
    name: str
    active: Optional[bool] = True


class TaskDetailCreate(TaskDetailBase):
    task_id: int


class TaskDetailResponse(TaskDetailBase):
    id: int
