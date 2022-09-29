from fastapi import APIRouter, Path, Depends

from api.services.auth import get_current_user
from api.services.users import UserService
from schemas.users import UserCreate, UserOut, UserUpdate


register_router = APIRouter(tags=['users'])
router = APIRouter(tags=['users'], dependencies=[Depends(get_current_user)])


@router.get("/users", response_model=list[UserOut])
async def list_users(service: UserService = Depends()):
    return await service.get_all_users()


@router.get('/users/{id}', response_model=UserOut)
async def retrieve_user(
        id: int = Path(..., description='The ID of the user', gt=0),
        service: UserService = Depends()
):
    return await service.get_user(user_id=id)


@register_router.post("/register", response_model=UserOut, status_code=201)
async def create_new_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)


@router.put('/users/{id}', response_model=UserOut)
async def update_user(
        user_data: UserUpdate,
        id: int = Path(..., description='The ID of the user', gt=0),
        service: UserService = Depends(),
):
    return await service.update_user(user_id=id, user=user_data)


@router.delete('/users/{id}', status_code=204)
async def destroy_user(
        id: int = Path(..., description='The ID of the user', gt=0),
        service: UserService = Depends(),
):
    return await service.delete_user(id)
