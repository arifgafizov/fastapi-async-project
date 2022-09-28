from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.services.auth import AuthService
from schemas.auth import Token, RefreshToken, AuthUser

router = APIRouter(tags=['auth'],)


@router.post('/auth', response_model=Token)
async def auth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.username, form_data.password)


@router.post('/token/refresh', response_model=Token)
async def refresh_token(
    token: RefreshToken,
    service: AuthService = Depends(),
):
    return await service.validate_refresh_token(token.refresh)


@router.post('/login', response_model=Token)
async def login(
    form_data: AuthUser,
    service: AuthService = Depends(),
):
    return await service.authenticate_user(form_data.email, form_data.password)
