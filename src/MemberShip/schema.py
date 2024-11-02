from pydantic import BaseModel

class MemberShipBaseModel(BaseModel):
    Memebership_id : int = 0
    Name : str = "string"


class AddUpdateMemberShip(BaseModel):
    Name : str = "string"