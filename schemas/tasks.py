from pydantic import BaseModel, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int
    user_id: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    @model_validator(mode='after')
    def check_name_or_pomodoro_count(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError('name or pomodoro_count is required')
        return self
