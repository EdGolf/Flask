from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime
from db import OrderStatus


class UserBase(BaseModel):
    firstname: str = Field(..., min_length=2, max_length=32)
    lastname: str = Field(..., min_length=2, max_length=32)
    email: EmailStr

    class Config:
        orm_mode = True


class UserIn(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(min_length=2, max_length=32)
    lastname: Optional[str] = Field(min_length=2, max_length=32)
    email: Optional[EmailStr]
    password: Optional[str] = Field(min_length=8, max_length=100)


class UserOut(UserBase):
    id: int


class GoodBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=2)
    price: Decimal = Field(..., max_digits=10, decimal_places=2, gt=0)

    class Config:
        orm_mode = True


class GoodIn(GoodBase):
    pass


class GoodOut(GoodBase):
    id: int


class GoodUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(min_length=2)
    price: Optional[Decimal] = Field(max_digits=10, decimal_places=2, gt=0)


class OrderBase(BaseModel):
    datetime_create: Optional[datetime.datetime] = Field(default_factory=lambda: datetime.datetime.now())
    status: Optional[OrderStatus] = Field(default=OrderStatus.OPEN)

    class Config:
        orm_mode = True


class OrderIn(OrderBase):
    user_id: int
    good_id: int


class OrderOut(OrderBase):
    id: int
    user: UserOut
    good: GoodOut


class OrderOutByUser(OrderBase):
    good: GoodOut


class OrderUpdate(BaseModel):
    datetime_create: Optional[datetime.datetime]
    status: Optional[OrderStatus]
    user_id: Optional[int]
    good_id: Optional[int]


class UserOrderOut(UserOut):
    orders: list[OrderOutByUser]