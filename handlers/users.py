from typing import Annotated

from fastapi import APIRouter, Depends

from dependency import get_users_service
from schemas import UserLogin, UserCreate
from service.users import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=UserLogin)
def create_user(
    user: UserCreate,
    users_service: Annotated[UserService, Depends(get_users_service)]
):
    return users_service.create_user(user.username, user.password)
