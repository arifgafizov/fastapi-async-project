from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from ..setup import Base
from .mixins import TimeStamp
from .enums import ContentType
from .users import User


class Section(TimeStamp, Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    course = relationship('Course', back_populates='sections')
    content_blocks = relationship('ContentBlock', back_populates='sections')


class ContentBlock(TimeStamp, Base):
    __tablename__ = 'content_blocks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ContentType))
    url = Column(URLType, nullable=True)
    content = Column(Text, nullable=True)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)
    sections = relationship('Section', back_populates='content_blocks')
    completed_content_blocks = relationship('CompletedContentBlock', back_populates='content_block')


class CompletedContentBlock(TimeStamp, Base):
    """
        This shows when a student has completed a content block.
    """
    __tablename__ = 'completed_content_blocks'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content_block_id = Column(Integer, ForeignKey('content_blocks.id'), nullable=False)
    url = Column(URLType, nullable=True)
    feedback = Column(Text, nullable=True)
    grade = Column(Integer, default=0)

    student = relationship(User, back_populates='student_content_blocks')
    content_block = relationship(ContentBlock, back_populates='completed_content_blocks')
