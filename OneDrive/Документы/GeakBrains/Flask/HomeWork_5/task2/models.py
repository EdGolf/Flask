from enum import StrEnum
from typing import Optional


class TaskStatus(StrEnum):
    TO_DO = 'todo'
    IN_PROCESS = 'in process'
    DONE = 'done'


class Task(BaseModel):
    title: str
    description: Optional[str]
    status: TaskStatus = TaskStatus.TO_DO


class TaskOut(Task):
    id: int


class TaskPut(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]