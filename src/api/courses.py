from fastapi import APIRouter, Depends, Path

from api.services.auth import get_current_user
from api.services.courses import CourseService
from schemas.courses import CourseOut, CourseCreate

router = APIRouter(tags=['courses'], dependencies=[Depends(get_current_user)])


@router.get('/courses', response_model=list[CourseOut])
async def list_courses(service: CourseService = Depends()):
    return await service.get_all_courses()


@router.post('/courses', response_model=CourseOut, status_code=201)
async def create_new_course(course: CourseCreate, service: CourseService = Depends()):
    return await service.create_course(course)


@router.get('/courses/{id}', response_model=CourseOut)
async def retrieve_course(
        id: int = Path(..., description='The ID of the course', gt=0),
        service: CourseService = Depends()
):
    return await service.get_course(course_id=id)


@router.put('/courses/{id}', response_model=CourseOut)
async def update_course(
        course_data: CourseCreate,
        id: int = Path(..., description='The ID of the user', gt=0),
        service: CourseService = Depends(),
):
    return await service.update_course(course_id=id, course=course_data)


@router.delete('/courses/{id}', status_code=204)
async def destroy_course(
        id: int = Path(..., description='The ID of the user', gt=0),
        service: CourseService = Depends(),
):
    return await service.delete_course(id)
