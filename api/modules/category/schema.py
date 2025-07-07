from pydantic import BaseModel, ConfigDict


class CategorySchema(BaseModel):
    id: int
    name: str
    active: bool
    model_config = ConfigDict(from_attributes=True)
