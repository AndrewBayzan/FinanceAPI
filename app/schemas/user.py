from pydantic import BaseModel, Field, EmailStr, SecretStr

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: SecretStr = Field(min_length=4)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"