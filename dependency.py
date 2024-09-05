from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.orm import Session

from cache import get_redis_connection
from database import get_db_session
from exceptions import InvalidTokenException, TokenExpiredException
from repository import TasksCache, TasksRepository, UsersRepository
from service import TasksService
from service.auth import AuthService
from service.users import UserService
from settings import Settings


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TasksRepository:
    return TasksRepository(db_session)


def get_tasks_cache_repository() -> TasksCache:
    return TasksCache(get_redis_connection())


def get_tasks_service(
    tasks_repo: TasksRepository = Depends(get_tasks_repository),
    tasks_cache: TasksCache = Depends(get_tasks_cache_repository),
) -> TasksService:
    return TasksService(
        tasks_repo=tasks_repo,
        tasks_cache=tasks_cache
    )


def get_users_repository(db_session: Session = Depends(get_db_session)) -> UsersRepository:
    return UsersRepository(db_session)


def get_auth_service(
    users_repo: UsersRepository = Depends(get_users_repository)
) -> AuthService:
    return AuthService(user_repo=users_repo, settings=Settings())


def get_users_service(
    users_repo: UsersRepository = Depends(get_users_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repo=users_repo, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        return auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
