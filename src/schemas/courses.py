from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    ...


class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
