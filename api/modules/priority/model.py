from db import BaseModel
from peewee import AutoField, TextField, BooleanField


class Priority(BaseModel):
    class Meta:
        table_name = "priority"

    id = AutoField(primary_key=True, null=False, default=5)
    importance = TextField(null=False, unique=True)
    active = BooleanField(default=True)


# importance
# 1	重要度高、緊急度高
# 2	重要度高、緊急度低
# 3	重要度低、緊急度高
# 4	重要度低、緊急度低
# 5 優先度なし
