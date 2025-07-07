from db import BaseModel
from peewee import AutoField, TextField, BooleanField


class Status(BaseModel):
    class Meta:
        table_name = "statuses"

    id = AutoField(primary_key=True)  # serial型、NOT NULL、主キー
    name = TextField(null=False)  # text型、NOT NULL (例: "未着手", "進行中", "完了")
    active = BooleanField(default=True, null=False)  # bool型、NOT NULL、デフォルトTRUE
