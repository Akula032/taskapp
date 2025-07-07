from peewee import AutoField, TextField, BooleanField, ForeignKeyField, DateField
from db import BaseModel
from modules.tasks.model import Task
from modules.status.model import Status
from modules.staff.model import Staff
from modules.priority.model import Priority


class TaskDetail(BaseModel):
    class Meta:
        table_name = "task_detail"

    id = AutoField(primary_key=True)

    task_id = ForeignKeyField(
        Task,
        backref="task_detail",
        column_name="tasks_id",
        null=False,
    )

    name = TextField(default="", null=False)

    staff = ForeignKeyField(
        Staff,
        column_name="staff_id",
        null=False,
    )

    status = ForeignKeyField(
        Status,
        column_name="status_id",
        backref="task_details",
        null=False,
        default=1,  # 1は未着手
    )
    priority = ForeignKeyField(
        Priority,
        column_name="priority_id",
        null=False,
    )
    start_date = DateField(
        column_name="start_date",
        null=True,
    )
    end_date = DateField(
        column_name="end_date",
        null=True,
    )
    active = BooleanField(default=True, null=False)
