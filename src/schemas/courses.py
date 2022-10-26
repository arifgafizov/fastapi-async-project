from typing import Optional

from pydantic import BaseModel, Field

from schemas.users import UserBaseOut


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


class CourseUsersOut(CourseOut):
    students: list[UserBaseOut] = []


class CourseStudent(BaseModel):
    course_id: int = Field(gt=0)
    student_id: int = Field(gt=0)
