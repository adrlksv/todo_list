from pydantic import BaseModel

from typing import Optional


class TaskModel(BaseModel):
    id: int
    task_name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
