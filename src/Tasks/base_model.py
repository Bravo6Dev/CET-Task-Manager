from pydantic import BaseModel, Field
from datetime import datetime

class TaskModel(BaseModel):
    task_id : int
    task_name : str
    description : str
    deadline : datetime
    status : int
    project_id : int

    class Config:
        from_attributes = True

class AddTask(BaseModel):
    task_name : str
    description : str | None = None
    deadline : datetime
    project_id : int

class UpdateTask(BaseModel):
    task_name : str = "string"
    description : str = "string"
    deadline : datetime = datetime.now()
    status : int = 0
    project_id : int = 0