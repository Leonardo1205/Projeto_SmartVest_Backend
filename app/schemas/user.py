from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    nickname: str = Field(min_length=2, max_length=60)
    email: EmailStr
    password: str = Field(min_length=6)

class UserRead(BaseModel):
    id: int
    nickname: str
    email: EmailStr

    class Config:
        from_attributes = True
