from db import BaseModel
from peewee import IntegerField, TextField, AutoField, BooleanField


class Login(BaseModel):
    class Meta:
        table_name = "login"

    id = AutoField(primary_key=True, null=False)
    staff_id = IntegerField(null=False)
    password = TextField(null=False)
    active = BooleanField(default=True)
