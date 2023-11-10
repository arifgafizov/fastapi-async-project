from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from ..setup import Base
from .mixins import TimeStamp


student_course = Table(
    'student_course',
    Base.metadata,
    Column("student_id", ForeignKey("users.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


class Course(TimeStamp, Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    sections = relationship('Section', back_populates='course', uselist=False)
    students = relationship('User', secondary='student_course', lazy='immediate', back_populates='courses')
