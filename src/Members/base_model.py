from pydantic import BaseModel, Field


class Members(BaseModel):
    memebr_id : int = 0
    FirstName : str = "string"
    LastName : str = "string"
    PhoneNumber : str | None = None
    membership_id : int = 0
    UserName : str = "string"
    Password : str = Field(exclude=True)

class AddUpdateMember(BaseModel):
    FirstName : str = "string"
    LastName : str = "string"
    PhoneNumber : str | None = None
    UserName : str = "string"
    Password : str = Field(exclude=True)
    membership_id : int = 0

class Login(BaseModel):
    username : str = "string"
    password : str = "string"