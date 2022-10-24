from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int


class CourseCreate(CourseBase):
    ...


class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True
