from db import BaseModel
from peewee import AutoField, DateTimeField, BooleanField


class Attendance(BaseModel):
    class Meta:
        table_name = "attendance"

    id = AutoField(primary_key=True)
    stamp_time = DateTimeField()
    is_check_in = BooleanField()
    # 出勤: True, 退勤: False
