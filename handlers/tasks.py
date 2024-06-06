from typing import Annotated

from fastapi import APIRouter, Depends

from dependency import get_tasks_repository, get_tasks_service
from repository import TasksRepository
from schemas.tasks import Task
from service import TasksService

router = APIRouter(prefix='/task', tags=['tasks'])


@router.get('/all', response_model=list[Task])
async def get_tasks(
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return task_service.get_tasks()


@router.get('/{task_id}', response_model=Task)
async def get_task(task_id: int, task_repo: Annotated[TasksRepository, Depends(get_tasks_repository)]):
    return task_repo.get_task(task_id)


@router.post('/', response_model=Task)
async def create_task(task: Task, task_repo: Annotated[TasksRepository, Depends(get_tasks_repository)]):
    task.id = task_repo.create_task(task)
    return task
