from pydantic import BaseModel, Field, EmailStr


class UserRequestAddSchema(BaseModel):
    email: EmailStr
    password: str


class UserAddSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPasswordSchema(UserSchema):
    hashed_password: str
