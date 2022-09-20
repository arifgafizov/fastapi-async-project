from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.users import UserService
from db.setup import get_session
from schemas.users import UserCreate, User, UserBase

router = APIRouter(tags=['users'],)


@router.get("/users", response_model=list[User])
async def list_users(service: UserService = Depends()):
    return await service.get_all_users()


@router.get('/users/{id}', response_model=User)
async def retrieve_user(
        id: int = Path(..., description='The ID of the user', gt=0),
        service: UserService = Depends()
):
    return await service.get_user(user_id=id)


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)


@router.put('/users/{id}', response_model=User)
async def update_user(
        user_data: UserBase,
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
