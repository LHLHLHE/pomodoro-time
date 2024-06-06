from dataclasses import dataclass

from repository import TasksRepository, TasksCache
from schemas.tasks import Task


@dataclass
class TasksService:
    tasks_repo: TasksRepository
    tasks_cache: TasksCache

    def get_tasks(self):
        if tasks := self.tasks_cache.get_tasks():
            return tasks
        else:
            tasks = self.tasks_repo.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            self.tasks_cache.set_tasks(tasks_schema)
            return tasks_schema
