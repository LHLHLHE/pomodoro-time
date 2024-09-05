from dataclasses import dataclass

from exceptions import TaskNotFound
from models import Tasks
from repository import TasksRepository, TasksCache
from schemas import TaskCreate
from schemas.tasks import Task


@dataclass
class TasksService:
    tasks_repo: TasksRepository
    tasks_cache: TasksCache

    def get_tasks(self) -> list[Task]:
        if tasks := self.tasks_cache.get_tasks():
            return tasks
        else:
            tasks = self.tasks_repo.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            self.tasks_cache.set_tasks(tasks_schema)
            return tasks_schema

    def get_task(self, task_id: int) -> Tasks | None:
        return self.tasks_repo.get_task(task_id)

    def create_task(self, task: TaskCreate, user_id: int) -> Task:
        task_id = self.tasks_repo.create_task(task, user_id)
        task = self.tasks_repo.get_task(task_id)
        return Task.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.tasks_repo.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFound()
        self.tasks_repo.delete_task(task_id=task_id, user_id=user_id)