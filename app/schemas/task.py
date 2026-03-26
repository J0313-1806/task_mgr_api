from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional
from enum import Enum as PyEnum
from ..models.task import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus = TaskStatus.TODO
    blocked_by_id: Optional[int] = Field(
        None, description="ID of another existing task that must be completed first"
    )
    # NEW: Position field (optional on create → will be auto-assigned)
    position: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None
    blocked_by_id: Optional[int] = None
    position: Optional[int] = None   # allow manual position update if needed

    model_config = ConfigDict(from_attributes=True)


class TaskRead(TaskBase):
    id: int
    blocked_by_id: Optional[int] = None
    position: int   # type: ignore # now always returned


# NEW: Schema for swapping two tasks
class TaskSwap(BaseModel):
    task_id1: int
    task_id2: int

    model_config = ConfigDict(from_attributes=True)