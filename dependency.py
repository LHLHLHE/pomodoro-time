from fastapi import Depends

from cache import get_redis_connection
from database import get_db_session
from repository import TasksCache, TasksRepository
from service import TasksService


def get_tasks_repository() -> TasksRepository:
    return TasksRepository(get_db_session())


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
