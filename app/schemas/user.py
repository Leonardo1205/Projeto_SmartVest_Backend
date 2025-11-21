from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    nickname: str = Field(min_length=2, max_length=60)
    email: EmailStr
    password: str = Field(min_length=6)

class UserRead(BaseModel):
    id: int
    nickname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
