# from ctypes.util import test
# from hmac import new
from db import db
from fastapi import HTTPException, status
from modules.tasks.model import Task as TaskModel
from modules.category.model import Category as CategoryModel
from modules.task_detail.model import TaskDetail as TaskDetailModel
from modules.status.model import Status as StatusModel
from modules.tasks.schema import TaskUpdate
from .schema import CompositeTaskCreate, DeleteTaskResponse
from peewee import JOIN, fn
from . import model
from modules.staff.model import Staff as StaffModel
from modules.priority.model import Priority as PriorityModel


def validate_create_task(new_title: str):
    # 新しい看板の列を作成する場合のみチェック
    existing_task_group = TaskModel.get_or_none(
        (TaskModel.title == new_title) & (TaskModel.active is True)
    )
    if existing_task_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"同じ名前のTaskの列「{new_title}」が既に存在します。",
        )


def get_tasks() -> list[TaskModel]:
    # アクティブなtasksテーブルだけをGetする
    tasks_query = (
        TaskModel.select(TaskModel, CategoryModel)
        .join(
            CategoryModel,
            JOIN.INNER,
            on=((TaskModel.category_id == CategoryModel.id) & (CategoryModel.active)),
        )
        .where(TaskModel.active)
        .order_by(TaskModel.id)
    )
    return list(tasks_query)


def create_composite_task(
    data: CompositeTaskCreate,
) -> TaskDetailModel:  # create_composite_task
    with db.atomic():
        target_category = None
        if data.category_id:  # 既存のカテゴリIDが送らてきた場合
            target_category = CategoryModel.get_or_none(
                CategoryModel.id == data.category_id
            )
            if not target_category:
                raise HTTPException(
                    status_code=404,
                    detail=f"カテゴリ: {data.category_id} が見つかりません。",
                )
        elif data.new_category_name:  # 新しいカテゴリ名が送られてきた場合
            # 同じ名前のカテゴリがあればそれを使用し、なければ新規作成 (Get or Create)
            target_category, created = CategoryModel.get_or_create(
                name=data.new_category_name, defaults={"active": True}
            )
        # タスクを確定させる
        target_task_group = None
        if data.task_id:  # 既存のTaskのIDが送られてきた場合
            target_task_group = TaskModel.get_or_none(TaskModel.id == data.task_id)
            if not target_task_group:
                raise HTTPException(
                    status_code=404, detail=f"タスク: {data.task_id} が見つかりません。"
                )
        elif data.new_task_title:  # 新しいTaskのタイトルが送られて来た場合
            if not target_category:
                raise HTTPException(
                    status_code=400,
                    detail="新しいTaskの列を作成するには、有効なカテゴリが必要です。",
                )
            target_task_group, created = TaskModel.get_or_create(
                title=data.new_task_title,  # このタイトルと
                category=target_category,  # このカテゴリの組み合わせで検索
                defaults={
                    "active": True
                },  # もし見つからなかった場合に、このデフォルト値で新規作成
            )
        if not target_task_group:
            raise HTTPException(
                status_code=400,
                detail="タスクカードを追加するための有効なTaskの列がありません。",
            )
        # 担当スタッフが存在するか検証
        target_staff = StaffModel.get_or_none(StaffModel.id == data.staff_id)
        if not target_staff:
            raise HTTPException(
                status_code=404,
                detail=f"担当スタッフ ID: {data.staff_id} が見つかりません。",
            )
        # 優先度が存在するか検証
        target_priority = PriorityModel.get_or_none(
            PriorityModel.id == data.priority_id
        )
        if not target_priority:
            raise HTTPException(
                status_code=404,
                detail=f"優先度 ID: {data.priority_id} が見つかりません。",
            )
        new_task_detail = TaskDetailModel.create(
            name=data.detail_name,
            task_id=target_task_group,  # モデルをtask_idにしたから変更
            staff_id=target_staff,  # スタッフオブジェクトを渡す
            status_id=data.status_id
            if data.status_id is not None
            else 1,  # ststus_idがあればそれを使うなければデフォルトの1
            priority=target_priority,
            start_date=data.start_date,  # 開始日
            end_date=data.end_date,  # 終了日
            active=True,
        )
        return new_task_detail


def get_all_tasks_and_details() -> list[TaskModel]:
    status_object = fn.jsonb_build_object(
        "id", StatusModel.id, "name", StatusModel.name, "active", StatusModel.active
    )
    category_object = fn.jsonb_build_object(
        "id",
        CategoryModel.id,
        "name",
        CategoryModel.name,
        "active",
        CategoryModel.active,
    )
    staff_object = fn.jsonb_build_object(
        "id",
        StaffModel.id,
        "code",
        StaffModel.code,
        "name",
        StaffModel.name,
        "active",
        StaffModel.active,
    )
    priority_object = fn.jsonb_build_object(
        "id", PriorityModel.id, "importance", PriorityModel.importance
    )
    detail_object = fn.array_agg(
        fn.jsonb_build_object(
            "id",
            TaskDetailModel.id,
            "task_id",
            TaskDetailModel.task_id,
            "name",
            TaskDetailModel.name,
            "status",
            status_object,
            "staff",
            staff_object,  # レスポンスにスタッフ追加
            "priority",
            priority_object,
            "start_date",
            TaskDetailModel.start_date,
            "end_date",
            TaskDetailModel.end_date,
            "active",
            TaskDetailModel.active,
        )
    ).order_by(TaskDetailModel.priority)
    # print(dir(detail_object)) これで、その変数に使える属性がわかる
    tasks_query = (
        TaskModel.select(
            TaskModel.id,
            TaskModel.title,
            TaskModel.active,
            category_object.alias("category"),
            detail_object.alias("task_detail"),
        )
        .join(
            CategoryModel,
            JOIN.INNER,
            on=(
                (TaskModel.category == CategoryModel.id)
                & (CategoryModel.active.__eq__(True))  # これだいじかも
            ),
        )
        .join(
            TaskDetailModel,
            JOIN.INNER,
            on=(
                (TaskDetailModel.task_id == TaskModel.id)
                & (TaskDetailModel.active.__eq__(True))
            ),
        )
        .join(
            StatusModel,
            JOIN.INNER,
            on=(
                (StatusModel.id == TaskDetailModel.status)
                & (StatusModel.active.__eq__(True))
            ),
        )
        .join(  # staffモデルをjoin
            StaffModel,
            JOIN.INNER,
            on=(TaskDetailModel.staff_id == StaffModel.id),
        )
        .join(
            PriorityModel,
            JOIN.INNER,
            on=(TaskDetailModel.priority_id == PriorityModel.id),
        )
        .where(TaskModel.active.__eq__(True))
        .group_by(TaskModel.id, CategoryModel.id)
        .order_by(TaskModel.id)
    )
    response = list(tasks_query.dicts())
    # print(response)
    return response


def update_task(
    task_body: TaskUpdate, original_detail: TaskDetailModel
) -> TaskDetailModel:
    # print(
    #     f"--- UPDATE受信: task_id={task_body.task_id}, title='{task_body.title}', status_id={task_body.status_id},priority_id={task_body.priority_id} ---"
    # )
    # データベースから、新しい所属先となるTask(列)を取得
    new_parent_task = TaskModel.get_or_none(TaskModel.id == task_body.task_id)
    # print(new_parent_task)

    if not new_parent_task:
        raise HTTPException(
            status_code=404,
            detail=f"移動先のタスクグループ ID: {task_body.task_id} が見つかりません。",
        )
    # もし新しいstaff_idがリクエストに含まれていたら、担当者を更新する

    if task_body.staff_id is not None:
        # 新しい担当スタッフが存在するか検証
        new_staff = StaffModel.get_or_none(StaffModel.id == task_body.staff_id)
        if not new_staff:
            raise HTTPException(
                status_code=404,
                detail=f"担当スタッフ ID: {task_body.staff_id} が見つかりません。",
            )
        # 担当者を更新
        original_detail.staff_id = new_staff

        # 優先度更新
    if task_body.priority_id is not None:
        new_priority = PriorityModel.get_or_none(
            PriorityModel.id == task_body.priority_id
        )
        if not new_priority:
            raise HTTPException(
                status_code=404,
                detail=f"優先度 ID: {task_body.priority_id} が見つかりません。",
            )
        original_detail.priority = new_priority

    # 受け取った情報で、元のタスク詳細オブジェクトを更新
    original_detail.task_id = task_body.task_id
    original_detail.name = task_body.title  # 'title' はカードの 'name' に対応
    original_detail.status_id = task_body.status_id
    original_detail.start_date = task_body.start_date
    original_detail.end_date = task_body.end_date
    # original_detail.task = new_parent_task  # 所属する列を新しいものに差し替え
    # 3. データベースに保存
    original_detail.save()
    # 4. 更新されたタスク詳細オブジェクトを返す
    return original_detail


def delete_task(task: model.Task) -> model.Task:
    # active フラグを False に設定
    task.active = False
    # 変更をデータベースに保存
    task.save()
    response = DeleteTaskResponse(id=task.id)
    return response
