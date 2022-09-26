from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.services.auth import AuthService
from schemas.auth import Token

router = APIRouter(tags=['auth'],)


@router.post('/login', response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.username, form_data.password)
