from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timezone
from modules.attendance.model import Attendance

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


class AttendanceResponse(BaseModel):
    id: int
    stamp_time: datetime
    is_check_in: bool

    class Config:
        orm_mode = True


@router.post(
    "/clock-in",
    # summary="出勤打刻を記録",
    status_code=status.HTTP_201_CREATED,
    response_model=AttendanceResponse,
)
def record_clock_in():
    try:
        current_time_utc = datetime.now(timezone.utc)
        new_record: Attendance = Attendance.create(
            stamp_time=current_time_utc, is_check_in=True
        )
        response = AttendanceResponse(
            id=new_record.id, stamp_time=current_time_utc, is_check_in=True
        )
        return response
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="出勤記録の保存中にエラーが発生しました。",
        )


@router.post(
    "/clock-out",
    # summary="退勤打刻を記録",
    status_code=status.HTTP_201_CREATED,
    response_model=AttendanceResponse,
)
def record_clock_out():
    try:
        current_time_utc = datetime.now(timezone.utc)
        new_record: Attendance = Attendance.create(
            stamp_time=current_time_utc, is_check_in=True
        )
        response = AttendanceResponse(
            id=new_record.id, stamp_time=current_time_utc, is_check_in=False
        )
        return response
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="退勤記録の保存中にエラーが発生しました。",
        )
