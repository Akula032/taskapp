from typing import List
from modules.priority.model import Priority


class PriorityService:
    @staticmethod
    def get_all_priorities() -> List[Priority]:
        return list(Priority.select().order_by(Priority.id))
