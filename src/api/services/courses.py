from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from db.models.courses import Course
from db.models.users import User
from db.setup import get_session
from schemas.courses import CourseCreate, CourseStudent


class CourseService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    def validate_course(self, course: Course):
        if course is None:
            raise HTTPException(status_code=404, detail='Course not found')

    async def _get(self, course_id: int):
        query = select(Course).where(Course.id == course_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_courses(self):
        result = await self.db.execute(select(Course).order_by(Course.id).options(selectinload(Course.students)))
        return result.scalars().all()

    async def get_course(self, course_id: int):
        course = await self._get(course_id)
        self.validate_course(course)
        return course

    async def create_course(self, course: CourseCreate):
        new_course = Course(
            title=course.title,
            description=course.description,
            )
        self.db.add(new_course)
        await self.db.flush()
        return await self._get(new_course.id)

    async def update_course(self, course_id: int, course: CourseCreate):
        db_course = await self._get(course_id)
        self.validate_course(db_course)
        q_course = update(Course).where(Course.id == course_id)
        q_course = q_course.values(title=course.title)
        q_course = q_course.values(description=course.description)

        await self.db.execute(q_course)
        await self.db.flush()
        return await self._get(course_id)

    async def delete_course(self, course_id: int):
        course = await self._get(course_id)
        self.validate_course(course)
        return await self.db.delete(course)

    async def add_user_to_course(self, data: CourseStudent):
        course = await self._get(data.course_id)
        user = await self.db.execute(select(User).where(User.id == data.student_id))
        user = user.scalar_one_or_none()
        course.students.append(user)
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
