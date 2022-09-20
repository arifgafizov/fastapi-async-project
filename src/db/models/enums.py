from enum import Enum


class Role(Enum):
    teacher = 1
    student = 2


class ContentType(Enum):
    lesson = 1
    quiz = 2
    assignment = 3