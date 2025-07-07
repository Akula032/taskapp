from peewee import AutoField, TextField, BooleanField, ForeignKeyField
from db import BaseModel
from modules.category.model import Category


class Task(BaseModel):
    class Meta:
        table_name = "tasks"

    id = AutoField(primary_key=True)
    title = TextField(default="", null=False)
    category = ForeignKeyField(
        Category, backref="tasks", column_name="category_id", null=False
    )
    active = BooleanField(default=True, null=False)
