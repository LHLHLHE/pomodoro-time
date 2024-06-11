from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
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
