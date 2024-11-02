from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.Members.sql_model import members
from src.Members.base_model import AddUpdateMember

from pydantic import BaseModel

from src.auth import utils

class MemeberService:
    def __convert_model_to_dict(self, model:BaseModel) -> dict:
        """
        Description
            Converts a Pydantic model to a dictionary representation.
        Parameters
            model (BaseModel): The Pydantic model to convert.
        Returns
            dict: A dictionary representation of the model's fields.
        Notes
            This function relies on the model_dump method provided by Pydantic's BaseModel.
            The function assumes that the input model inherits from BaseModel.
        """
        return model.model_dump()

    async def get_all(self, session: AsyncSession) -> list:
        try:
            from src.MemberShip.sql_model import MemeberShip
            # Select all members with their associated membership name
            query = select(members.memebr_id,
                        members.FirstName, 
                        members.LastName,
                        members.PhoneNumber,
                        members.UserName,
                        MemeberShip.Name).join(MemeberShip, members.membership_id == MemeberShip.Memebership_id)

            result = await session.execute(query)
            rows = result.all()
            data = [
                {
                    "Id": row.memebr_id,
                    "FirstName": row.FirstName,
                    "LastName": row.LastName,
                    "PhoneNumber": row.PhoneNumber,
                    "UserName": row.UserName,
                    "Membership": row.Name
                }
                for row in rows
            ]
            return data
        except Exception as ex:
            raise ex

    async def get_by_id(self, Id:int, session:AsyncSession):        
        try:
            statement = select(members).where(members.memebr_id == Id)
            return (await session.execute(statement)).scalar_one_or_none()
        except Exception as ex:
            raise ex

    async def add(self, memebr_data:AddUpdateMember, session:AsyncSession):
        try:
            # check if the member model is none or not
            if not memebr_data:
                return None
            if await self.exist_username(memebr_data.UserName, session):
                raise Exception("Username already exists")
            # convert the model to dict 
            memebr_data_to_dict = self.__convert_model_to_dict(memebr_data)

            # fill the table model with data
            new_member = members(**memebr_data_to_dict)

            # hash the password
            new_member.Password = utils.hash(memebr_data.Password)

            # add the member
            session.add(new_member)
            await session.commit()
            # return the new member with his id
            member_dict = new_member.__dict__
            member_dict.pop('Password', None)
            return member_dict
        except Exception as ex:
            raise ex

    async def update(self, Id:int, memebr_data:AddUpdateMember, session:AsyncSession):
        try:
            # get the member you want to update by his id
            member_to_update = await self.get_by_id(Id, session)
            # check if one of models are None
            if not memebr_data or not member_to_update:
                return None
            # convert member_data model to dict
            memebr_data_to_dict = self.__convert_model_to_dict(memebr_data)

            if member_to_update.UserName != memebr_data.UserName and await self.exist_username(memebr_data.UserName, session):
                raise Exception("Username already exists")

            memebr_data_to_dict["Password"] = utils.hash(memebr_data.Password)

            # make a loop for key and value
            for k, v in memebr_data_to_dict.items():
                # fill the member_to_update object with new values
                setattr(member_to_update, k, v)
            await session.commit()
            await session.refresh(member_to_update)
            member_dict = member_to_update.__dict__
            member_dict.pop('Password', None)
            return member_dict
        except Exception as ex:
            raise ex

    async def delete(self, Id:int, session:AsyncSession):
        try:
            # get member to delete
            member_to_delete = await self.get_by_id(Id, session)
            if not member_to_delete:
                return None
            await session.delete(member_to_delete)
            await session.commit()
            return {"Message" : "Member Deleted Successfully"} 
        except Exception as ex:
            raise ex

    async def get_member_by_username(self, username:str, session:AsyncSession):
        try:
            statement = select(members).options(selectinload(members.membership)).where(members.UserName == username)
            result = await session.execute(statement)
            return result.scalars().one_or_none()
        except Exception as ex:
            raise ex

    async def exist_username(self, username:str, session:AsyncSession):
        try:
            user = await self.get_member_by_username(username, session)
            return False if user is None else True
        except Exception as ex:
            raise ex