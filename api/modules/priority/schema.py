from pydantic import BaseModel, ConfigDict


class PrioritySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    importance: str
