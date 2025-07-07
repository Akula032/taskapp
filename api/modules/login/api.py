from typing import Optional
from email import message
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modules.staff.model import Staff
from modules.login.model import Login

router = APIRouter(prefix="/login")


class LoginRequest(BaseModel):
    code: str
    password: str


class LoginCreateResponse(BaseModel):
    message: str
    staff_name: Optional[str]


@router.post("", response_model=LoginCreateResponse)
def login(request: LoginRequest):
    staff = Staff.get_or_none(Staff.code == request.code, Staff.active)
    if not staff:
        raise HTTPException(status_code=401, detail="IDまたはパスワードが違います。")
    login = Login.get_or_none(Login.staff_id == staff.id, Login.active)
    if not login or login.password != request.password:
        raise HTTPException(status_code=401, detail="IDまたはパスワードが違います。")
    response = LoginCreateResponse(message="ログイン成功", staff_name=staff.name)
    return response
