from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship

from ..setup import Base
from .enums import Role
from .mixins import TimeStamp


class User(TimeStamp, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Enum(Role))
    password_hash = Column(Text)

    profile = relationship('Profile', back_populates='owner', uselist=False, cascade="all,delete")
    student_courses = relationship('StudentCourse', back_populates='student')
    student_content_blocks = relationship('CompletedContentBlock', back_populates='student')

    def __repr__(self):
        return f'{self.id}-{self.email}'


users = User.__table__


class Profile(TimeStamp, Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)
    users_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('User', back_populates='profile')


profiles = Profile.__table__
