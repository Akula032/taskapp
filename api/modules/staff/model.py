from db import BaseModel
from peewee import TextField, AutoField, BooleanField, CharField


class Staff(BaseModel):
    class Meta:
        table_name = "staff"

    id = AutoField(primary_key=True, null=False)
    code = CharField(max_length=6, null=False, unique=True)
    name = TextField(null=False)
    active = BooleanField(default=True)
