from pydantic import BaseModel
from datetime import datetime
import pydantic

class Project_model(BaseModel):
    project_id : int
    project_Name : str
    deadline : datetime
    @pydantic.field_validator("project_Name")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the project name")
        return value
    @pydantic.field_validator("deadline")
    def valid_deadline(value:datetime):
        if value < datetime.now():
            raise Exception("Deadline cannot be in the past")
        return value

class AddUpdateProject(BaseModel):
    project_Name : str
    deadline : datetime

