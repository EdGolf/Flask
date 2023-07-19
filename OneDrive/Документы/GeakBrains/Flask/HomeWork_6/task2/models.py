from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: str
    done: bool = False


class TaskIn(TaskBase):
    pass


class TaskOut(TaskBase):
    id: str


class TaskUpdate(BaseModel):
    title: str | None
    description: str | None
    done: bool | None