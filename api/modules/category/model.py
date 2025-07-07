from peewee import AutoField, TextField, BooleanField
from db import BaseModel


class Category(BaseModel):
    class Meta:
        table_name = "category"

    id = AutoField(primary_key=True)
    name = TextField(null=False)
    active = BooleanField(default=True, null=False)
