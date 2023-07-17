from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserPut(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]