from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    code: str
    description: str
    credits: int


class CourseUpdate(BaseModel):
    title: str
    code: str
    description: str
    credits: int


class CourseOut(BaseModel):
    id: int
    title: str
    code: str
    description: str
    credits: int

    class Config:
        from_attributes = True