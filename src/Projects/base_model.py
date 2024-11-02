from pydantic import BaseModel
from datetime import datetime


class Project_model(BaseModel):
    project_id : int
    project_Name : str
    deadline : datetime

class AddUpdateProject(BaseModel):
    project_Name : str
    deadline : datetime

