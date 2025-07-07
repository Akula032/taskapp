from db import db


# from modules.login.model import Login
from modules.tasks.model import Task
from modules.staff.model import Staff

# from modules.attendance.model import Attendance
from modules.task_detail.model import TaskDetail
from modules.category.model import Category
from modules.status.model import Status
from modules.priority.model import Priority

# class BaseModel(Model):
#     class Meta:
#         database = db


def reset_database():
    db.drop_tables(
        [Staff, Category, Task, TaskDetail, Priority, Status], safe=True, cascade=True
    )
    print("テーブルのデータを削除しました")
    db.create_tables([Staff, Category, Task, TaskDetail, Priority, Status], safe=True)
    print("新しくテーブルを作成しました")


# DBeaverややこしくなるからLogin,Attendanceは削除


def seed_initial_data():
    print("初期データを入れます")
    with db.atomic():
        if Status.select().count() == 0:
            status_data = [
                {"id": 1, "name": "未着手", "active": True},
                {"id": 2, "name": "進行中", "active": True},
                {"id": 3, "name": "完了", "active": True},
            ]
            Status.insert_many(status_data).execute()
            print("Status_データを挿入しました")
        if Priority.select().count() == 0:
            priority_data = [
                {"id": 1, "importance": "重要度高、緊急度高"},
                {"id": 2, "importance": "重要度高、緊急度低"},
                {"id": 3, "importance": "重要度低、緊急度高"},
                {"id": 4, "importance": "重要度低、緊急度低"},
                {"id": 5, "importance": "重要度なし"},
            ]
            Priority.insert_many(priority_data).execute()
            print("Priorty_データを挿入しました")


# importance
# 1	重要度高、緊急度高
# 2	重要度高、緊急度低
# 3	重要度低、緊急度高
# 4	重要度低、緊急度低
# 5 優先度なし

if __name__ == "__main__":
    reset_database()
    seed_initial_data()
