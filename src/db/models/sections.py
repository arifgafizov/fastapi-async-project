from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ..setup import Base
from .mixins import TimeStamp


# class Section(TimeStamp, Base):
#     __tablename__ = 'sections'
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#     course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
#
#     course = relationship('Course', back_populates='sections')
#     content_blocks = relationship('ContentBlock', back_populates='section')
