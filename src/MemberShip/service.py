from MemberShip.schema import AddUpdateMemberShip
from MemberShip.sql_model import MemeberShip
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

class MemberShipService:
    def __convert_model_to_dict(self, model:BaseModel):
        return model.model_dump()

    async def get_all(delf, session:AsyncSession):
        try:
            query = select(MemeberShip)
            result = await session.execute(query)

            return result.scalars().all()
        except Exception as ex:
            raise ex

    async def get_by_id(self, Id:int, session:AsyncSession):
        try:
            query = select(MemeberShip).where(MemeberShip.Memebership_id == Id)
            return (await session.execute(query)).scalar_one_or_none()
        except Exception as ex:
            raise ex

    async def add(self, memebrship_data:AddUpdateMemberShip, session:AsyncSession):
        try:
            # check if the member model is none or not
            if not memebrship_data:
                return None
            # convert the model to dict 
            memebrship_data_to_dict = self.__convert_model_to_dict(memebrship_data)

            # fill the table model with data
            new_membership = MemeberShip(**memebrship_data_to_dict)
            # add the member
            session.add(new_membership)
            await session.commit()
            # return the new member with his id
            return new_membership
        except Exception as ex:
            raise ex

    async def update(self, Id:int, memebrship_data:AddUpdateMemberShip, session:AsyncSession):
        try:
            # get the member you want to update by his id
            membership_to_update = await self.get_by_id(Id, session)
            # check if one of models are None
            if not memebrship_data or not membership_to_update:
                return None
            # convert member_data model to dict
            memebrship_data_to_dict = self.__convert_model_to_dict(memebrship_data)
            # make a loop for key and value
            for k, v in memebrship_data_to_dict.items():
                # fill the member_to_update object with new values
                setattr(membership_to_update, k, v)
            await session.commit()
            await session.refresh(membership_to_update)
            return membership_to_update
        except Exception as ex:
            raise ex

    async def delete(self, Id:int, session:AsyncSession):
        try:
            # get member to delete
            membership_to_delete = await self.get_by_id(Id, session)
            if not membership_to_delete:
                return None
            await session.delete(membership_to_delete)
            await session.commit()
            return {"Message" : "Membership Deleted Successfully"} 
        except Exception as ex:
            raise ex