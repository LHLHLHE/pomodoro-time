from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from dependency import get_tasks_service, get_request_user_id
from exceptions import TaskNotFound
from schemas import Task, TaskCreate
from service import TasksService

router = APIRouter(prefix='/task', tags=['tasks'])


@router.get('/all', response_model=list[Task])
async def get_tasks(
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return task_service.get_tasks()


@router.get('/{task_id}', response_model=Task | None)
async def get_task(
    task_id: int,
    task_service: Annotated[TasksService, Depends(get_tasks_service)]
):
    return task_service.get_task(task_id)


@router.post('/', response_model=Task)
async def create_task(
    body: TaskCreate,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    return task_service.create_task(body, user_id)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        task_service.delete_task(task_id, user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
