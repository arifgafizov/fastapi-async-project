from fastapi import APIRouter

router = APIRouter(tags=['courses'],)


@router.get('/courses')
async def read_courses():
    return {'courses': []}


@router.post('/courses')
async def create_course():
    return {'courses': []}


@router.get('/courses/{id}')
async def read_course():
    return {'courses': []}


@router.put('/courses/{id}')
async def update_course():
    return {'courses': []}


@router.delete('/courses/{id}')
async def delete_course():
    return {'courses': []}
