from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import Tasks, Categories
from schemas.tasks import Task


class TasksRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> list[Tasks]:
        with self.db_session() as session:
            tasks: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return tasks

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: Tasks = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session() as session:
            task: Tasks = session.execute(query).scalars().all()
        return task

    def create_task(self, task: Task) -> int:
        db_task = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(db_task)
            session.commit()
            return db_task.id

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id))
            session.commit()
