from Tasks.sql_model import Task
from Tasks.base_model import AddTask

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel


class TaskService:

    def __convert_model_to_dict(self, model:BaseModel) -> dict:
        return model.model_dump()

    async def get_all(self, session: AsyncSession):
        try:
            query = select(Task)
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as ex:
            raise ex   

    async def add(self, task_data:AddTask, session:AsyncSession):
        try:
            # check if the task model is none or not
            if task_data is None:
                return None
            task_data_to_dict = self.__convert_model_to_dict(task_data)
            new_task = Task(**task_data_to_dict)
            new_task.status = 0
            session.add(new_task)
            await session.commit()
            return new_task
        except Exception as ex:
            raise ex

    async def get_by_id(self, id:int, session:AsyncSession):
        try:
            query = select(Task).where(Task.task_id == id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
        except Exception as ex:
            raise ex

    async def delete(self, id:int, session:AsyncSession):
        try:
            # get task to delete
            task_to_delete = await self.get_by_id(id, session)
            if not task_to_delete:
                return None
            await session.delete(task_to_delete)
            await session.commit()
            return {"Message" : "Task Deleted Successfully"} 
        except Exception as ex:
            raise ex

    async def update(self, id:int, task_data:AddTask, session:AsyncSession):
        try:
            task_to_update = await self.get_by_id(id, session)
            if not task_to_update:
                return None
            task_data_to_dict = self.__convert_model_to_dict(task_data)
            for key, value in task_data_to_dict.items():
                setattr(task_to_update, key, value)
            await session.commit()
            return task_to_update
        except Exception as ex:
            raise ex