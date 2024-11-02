from src.Projects.sql_model import Project
from src.Projects.base_model import AddUpdateProject

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class ProjectService:
    def __convert_model_to_dict(self, model:BaseModel) -> dict:
        return model.model_dump()

    async def get_all(self, session: AsyncSession) -> list:
        try:
            query = select(Project)
            result = await session.execute(query)
            return result.scalars().all()   
        except Exception as ex:
            raise ex

    async def get_by_id(self, id:int, session:AsyncSession) -> dict:
        try:
            query = select(Project).where(Project.project_id == id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
        except Exception as ex:
            raise ex

    async def add(self, project_data:AddUpdateProject, session:AsyncSession):
        try:
            # check if the member model is none or not
            if not project_data:
                return None
            # convert the model to dict 
            project_data_to_dict = self.__convert_model_to_dict(project_data)

            # fill the table model with data
            new_project = Project(**project_data_to_dict)
            # add the member
            session.add(new_project)
            await session.commit()
            # return the new member with his id
            return new_project
        except Exception as ex:
            raise ex

    async def delete(self, id:int, session:AsyncSession):
        try:
            # get member to delete
            project_to_delete = await self.get_by_id(id, session)
            if not project_to_delete:
                return None
            await session.delete(project_to_delete)
            await session.commit()
            return {"Message" : "Project Deleted Successfully"}
        except Exception as ex:
            raise ex

    async def update(self, id:int, project_data:AddUpdateProject, session:AsyncSession):
        try:
            project_to_update = await self.get_by_id(id, session)
            if not project_to_update:
                return None
            project_data_to_dict = self.__convert_model_to_dict(project_data)
            for key, value in project_data_to_dict.items():
                setattr(project_to_update, key, value)
            await session.commit()
            return project_to_update
        except Exception as ex:
            raise ex