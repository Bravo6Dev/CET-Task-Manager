from pydantic import BaseModel, Field
from datetime import datetime
import pydantic

class TaskModel(BaseModel):
    task_id : int
    task_name : str
    description : str
    deadline : datetime
    status : int
    project_id : int
    @pydantic.field_validator("task_name")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the task name")
        return value
    @pydantic.field_validator("deadline")
    def valid_deadline(value:datetime):
        if value < datetime.now():
            raise Exception("Deadline cannot be in the past")
        return value

    class Config:
        from_attributes = True

class AddTask(BaseModel):
    task_name : str
    description : str | None = None
    deadline : datetime = datetime.now()
    project_id : int
    
    @pydantic.field_validator("task_name")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the task name")
        return value
    @pydantic.field_validator("deadline")
    def valid_deadline(value:datetime):
        if value < datetime.now():
            raise Exception("Deadline cannot be in the past")
        return value

class UpdateTask(BaseModel):
    task_name : str = "string"
    description : str = "string"
    deadline : datetime = datetime.now()
    status : int = 0
    project_id : int = 0
    @pydantic.field_validator("task_name")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the task name")
        return value
    @pydantic.field_validator("deadline")
    def valid_deadline(value:datetime):
        if value < datetime.now():
            raise Exception("Deadline cannot be in the past")
        return value
    @pydantic.field_validator("status")
    def valid_status(value:int):
        if value < 0:
            raise Exception("Status cannot be negative")
        return value