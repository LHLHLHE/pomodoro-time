from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette import status

from dependency import get_auth_service
from exceptions import UserNotFoundException, UserIncorrectPasswordException
from schemas import UserLogin, UserCreate
from service.auth import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=UserLogin)
def login(
    user: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(user.username, user.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.get('/login/google', response_class=RedirectResponse)
def login_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/google')
def auth_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.auth_google(code=code)


@router.get('/login/yandex', response_class=RedirectResponse)
def login_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/yandex')
def auth_yandex(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.auth_yandex(code=code)
