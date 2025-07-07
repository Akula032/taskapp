from fastapi import APIRouter, HTTPException
import modules.tasks.schema as task_schema
import modules.tasks.service as task_crud
from modules.task_detail.model import TaskDetail as TaskDetailModel
from modules.task_detail.schema import TaskDetailResponse
from modules.tasks.schema import TasksResponse
from typing import List

router = APIRouter(prefix="/tasks")


@router.get("", response_model=list[task_schema.Task])
def list_tasks():
    return task_crud.get_all_tasks_and_details()


@router.get(
    "/with_category",
    response_model=List[TasksResponse],
    summary="タスクグループの一覧を取得",
    tags=["Tasks"],
)
def list_simple_tasks():
    return task_crud.get_tasks()


@router.post(
    "",
    response_model=TaskDetailResponse,
    summary="タスクの追加",
    tags=["Task"],
)
def create_task_endpoint(task_body: task_schema.CompositeTaskCreate):
    return task_crud.create_composite_task(task_body)


# TaskCreateResponseをTaskUpdateResponseに変更
# TaskCreateをTaskUpdateに変更
# task_idをtask_detail_idに変更
@router.put(
    "/{task_detail_id}",
    response_model=TaskDetailResponse,
    summary="task_detailの編集",
    tags=["Task"],
)
def update_task(task_detail_id: int, task_body: task_schema.TaskUpdate):
    # サービスを呼び出さず、ここで直接Peeweeを使ってDBからタスク詳細を取得
    task_to_update = TaskDetailModel.get_or_none(TaskDetailModel.id == task_detail_id)
    updated_task = task_crud.update_task(task_body, original_detail=task_to_update)
    return updated_task


# @router.put("/{task_id}", response_model=task_schema.TaskDeleteResponse)
# def delete_task(task_id: int):
#     task = task_crud.get_task(task_id=task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task_crud.delete_task(task)


@router.patch(
    "/{task_id}",
    response_model=task_schema.DeleteTaskResponse,
    summary="task_detailの非アクティブ化",
    tags=["Task"],
)
def delete_task_endpoint(task_id: int):
    task = TaskDetailModel.get_or_none(TaskDetailModel.id == task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_crud.delete_task(task=task)
