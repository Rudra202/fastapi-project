from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    age: int
    department: str


class StudentUpdate(BaseModel):
    full_name: str
    email: EmailStr
    age: int
    department: str


class StudentOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    age: int
    department: str

    class Config:
        from_attributes = True