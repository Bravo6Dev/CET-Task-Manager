from pydantic import BaseModel


class MemberInTaskModel(BaseModel):
    task_id : int
    member_id : int

class AddUpdateMemberInTask(BaseModel):
    task_id : int
    member_id : int
