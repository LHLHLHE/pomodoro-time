from pydantic import BaseModel, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_name_or_pomodoro_count(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError()
        return self
