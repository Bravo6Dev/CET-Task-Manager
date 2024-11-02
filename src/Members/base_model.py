from pydantic import BaseModel, Field
import pydantic


class Members(BaseModel):
    memebr_id : int = 0
    FirstName : str = "string"
    LastName : str = "string"
    PhoneNumber : str | None = None
    membership_id : int = 0
    UserName : str = "string"
    Password : str = Field(exclude=True)
    
    @pydantic.field_validator("FirstName", "LastName", "UserNane")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the name or username")
    @pydantic.field_validator("Password")
    def valid_password(value:str):
        if value is None or value == "":
            raise Exception("Please enter the password")
        elif len(value) < 8:
            raise Exception("Password must be at least 8 characters")
        return value

class AddUpdateMember(BaseModel):
    FirstName : str = "string"
    LastName : str = "string"
    PhoneNumber : str | None = None
    UserName : str = "string"
    Password : str = Field(exclude=True)
    membership_id : int = 0
    @pydantic.field_validator("FirstName", "LastName", "UserNane")
    def valid_name(value:str):
        if value is None or value == "":
            raise Exception("Please enter the name or username")
    @pydantic.field_validator("Password")
    def valid_password(value:str):
        if value is None or value == "":
            raise Exception("Please enter the password")
        elif len(value) < 8:
            raise Exception("Password must be at least 8 characters")
        return value

class Login(BaseModel):
    username : str = "string"
    password : str = "string"