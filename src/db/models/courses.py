from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..setup import Base
from .users import User
from .mixins import TimeStamp


class Course(TimeStamp, Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    sections = relationship('Section', back_populates='course', uselist=False)
    student_courses = relationship('StudentCourse', back_populates='course')


class StudentCourse(TimeStamp, Base):
    """
        Students can be assigned to courses
    """
    __tablename__ = 'student_courses'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    completed = Column(Boolean, default=False)

    student = relationship(User, back_populates='student_courses')
    course = relationship('Course', back_populates='student_courses')
