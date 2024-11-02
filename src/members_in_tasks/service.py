from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from members_in_tasks.sql_model import MembersInTasks
from members_in_tasks.base_model import AddUpdateMemberInTask

from pydantic import BaseModel

class MemberInTaskService:

    def __convert_model_to_dict(self, model:BaseModel) -> dict:
        return model.model_dump()

    async def __get_by_id_sql_model(self, id:int, session:AsyncSession):
        try:
            query = select(MembersInTasks).where(MembersInTasks.id == id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
        except Exception as ex: 
            raise ex

    async def get_all(self, session: AsyncSession):
        try:
            from src.Members.sql_model import members
            from Tasks.sql_model import Task

            query = select(MembersInTasks.id, func.concat(members.FirstName, " ", members.LastName).label("full_name"),
                    Task.task_name, Task.deadline).join(members, 
                    MembersInTasks.member_id == members.memebr_id).join(Task,
                    MembersInTasks.task_id == Task.task_id)

            result = await session.execute(query)
            rows = result.all()
            data = [
                {
                    "id": row.id,
                    "full_name": row.full_name,
                    "task_name": row.task_name,
                    "deadline": row.deadline
                }
                for row in rows
            ]
            return data
        except Exception as ex:
            raise ex
    async def get_by_id(self, id:int, session:AsyncSession):
        try:
            from src.Members.sql_model import members
            from Tasks.sql_model import Task
            
            query = select(MembersInTasks.id, func.concat(members.FirstName, " ", members.LastName).label("full_name"),
                    Task.task_name, Task.deadline).join(members, 
                    MembersInTasks.member_id == members.memebr_id).join(Task,
                    MembersInTasks.task_id == Task.task_id).where(MembersInTasks.id == id)
            result = await session.execute(query)
            row = result.one_or_none()
            data = {
                "id": row.id,
                "full_name": row.full_name,
                "task_name": row.task_name,
                "deadline": row.deadline
            }
            return data
        except Exception as ex:
            raise ex

    async def add(self, model:AddUpdateMemberInTask, session:AsyncSession):
        try:
            # check if the member model is none or not
            if model is None:
                return None
            # convert the model to dict 
            model_to_dict = self.__convert_model_to_dict(model)

            # fill the table model with data
            table_model = MembersInTasks(**model_to_dict)
            # add the member
            session.add(table_model)
            await session.commit()
            return table_model
        except Exception as ex:
            raise ex

    async def update(self, id:int, model:AddUpdateMemberInTask, session:AsyncSession):
        try:
            data = await self.__get_by_id_sql_model(id, session)
            if data is None:
                return None
            model_to_dict = self.__convert_model_to_dict(model)
            for key, value in model_to_dict.items(): 
                setattr(data, key, value)
            await session.commit()
            return data
        except Exception as ex:
            raise ex

    async def delete(self, id:int, session:AsyncSession):
        try:
            data = await self.__get_by_id_sql_model(id, session)
            if data is None:
                return None
            await session.delete(data)
            await session.commit()
            return {"Message" : "Member in this task Deleted Successfully"}
        except Exception as ex:
            raise ex