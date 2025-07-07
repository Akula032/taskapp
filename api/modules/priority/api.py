from typing import List
from fastapi import APIRouter
from modules.priority.schema import PrioritySchema
from modules.priority.service import PriorityService

router = APIRouter()


@router.get(
    "",
    response_model=List[PrioritySchema],
    summary="優先度リストを取得",
    tags=["Priority"],
)
def list_priorities():
    return PriorityService.get_all_priorities()
