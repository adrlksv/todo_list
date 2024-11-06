from pydantic import BaseModel, Field

from typing import Optional


class TaskModel(BaseModel):
    id: int
    task_name: str = Field(example="New task")
    description: Optional[str] = None
