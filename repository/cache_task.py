import json

from redis import Redis

from schemas.tasks import Task


class TasksCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[Task]:
        with self.redis as redis:
            return [Task.model_validate(
                json.loads(task) for task in redis.lrange('tasks', 0, -1)
            )]

    def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.json() for task in tasks]
        with self.redis as redis:
            redis.lpush('tasks', *tasks_json)
