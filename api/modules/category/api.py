from fastapi import APIRouter
from typing import List  # Listは古い
from modules.category.schema import CategorySchema
import modules.category.service as category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategorySchema])
def list_statuses():
    return category.get_all_categories()
