from peewee import PostgresqlDatabase, Model
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
NAME = os.getenv("DB_NAME")

db = PostgresqlDatabase(
    database='demo',
    user='postgres',
    password='postgres',
    host='db',
    port=5432,
)

# db = PostgresqlDatabase(
#     database='demo',
#     user='postgres',
#     password='D2bI9usWIs2BMr5c08tq',
#     host='database-1.cdg8ywe649dz.ap-northeast-3.rds.amazonaws.com',
#     port=5432,
# )


class BaseModel(Model):
    class Meta:
        database = db


def get_db():
    try:
        db.connect()
        yield
    finally:
        db.close()
