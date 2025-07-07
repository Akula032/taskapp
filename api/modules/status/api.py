from fastapi import APIRouter
from typing import List
from . import schema as status_schema
from . import service as status_crud

router = APIRouter(prefix="/statuses", tags=["Statuses"])

@router.get("", response_model=List[status_schema.StatusSchema])
def list_statuses():
    return status_crud.get_all_statuses()
