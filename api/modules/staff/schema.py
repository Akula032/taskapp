from pydantic import BaseModel, Field
from typing import Optional


# codeは文字列で取得
class StaffCreateSchema(BaseModel):
    # FastAPIの機能で、正規表現の条件以外だったら422エラーを返す
    code: str = Field(..., pattern=r"^[0-9]{6}$", description="職員ID (6桁)")
    name: str = Field(..., description="職員名")


class StaffResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    active: bool

    class Config:
        from_attributes = True


class StaffUpdateSchema(BaseModel):
    # 更新したい項目だけを送れるように、全てのフィールドを任意項目(Optional)にする
    code: Optional[str] = Field(
        None, pattern=r"^[0-9]{6}$", description="職員ID（数字6桁）"
    )
    name: Optional[str] = Field(None, description="職員名")
