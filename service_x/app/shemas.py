from typing import Optional, List
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    number: int
    status: str
    result: Optional[int]


class AllTasksResponse(BaseModel):
    tasks: List[TaskSchema]
