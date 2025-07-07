import pytest
from fastapi.testclient import TestClient
from main import app
from db import db
from modules.tasks.model import Task, Done
from peewee import Proxy, SqliteDatabase


db = Proxy()
# テスト用DBの設定
TEST_DB = SqliteDatabase(":memory:")


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    # テスト用DBに接続
    db.initialize(TEST_DB)
    TEST_DB.connect()
    TEST_DB.create_tables([Task, Done])
    yield
    # テスト終了後にデータベースの初期化
    TEST_DB.drop_tables([Task, Done])
    TEST_DB.close()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_and_read(client):
    # タスクを作成
    response = client.post("/tasks", json={"title": "テストタスク"})
    assert response.status_code == 200
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"

    # タスクを取得
    response = client.get("/tasks")
    assert response.status_code == 200
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "テストタスク"
    assert response_obj[0]["done"] is False


def test_done_flag(client):
    # タスクを作成
    response = client.post("/tasks", json={"title": "テストタスク2"})
    assert response.status_code == 200
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク2"

    # 完了フラグを立てる
    response = client.put("/tasks/1/done")
    assert response.status_code == 200

    # すでに完了フラグが立っているので400を返す
    response = client.put("/tasks/1/done")
    assert response.status_code == 400

    # 完了フラグを外す
    response = client.delete("/tasks/1/done")
    assert response.status_code == 200

    # すでに完了フラグが外れているので404を返す
    response = client.delete("/tasks/1/done")
    assert response.status_code == 404
