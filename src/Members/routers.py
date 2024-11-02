from fastapi import APIRouter, Depends, status
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from db.db_context import get_session

from Members.service import MemeberService
from Members.base_model import AddUpdateMember
from Members.base_model import Login

from auth.dependencies import AccessTokenBearer, RolesChecker
from auth.utils import create_token, verfiy_password

member_router = APIRouter(prefix='/members', tags=["Members"])
service = MemeberService()
access_token_bearer = AccessTokenBearer()
admin_access = RolesChecker(["Leader", "Ass. Leader"])
users_access = RolesChecker(["Leader", "Ass. Leader", "Memebr"])

@member_router.get("/getall")
async def get_all(session:AsyncSession = Depends(get_session), 
                user_details = Depends(access_token_bearer),
                permissions = Depends(users_access)):
    try:
        data = await service.get_all(session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        return JSONResponse(status_code=500, content={"message": str(ex)})


@member_router.get("/get/{Id}")
async def get_by_id(Id:int, session:AsyncSession = Depends(get_session), 
                    user_dtails = Depends(access_token_bearer),
                    admin = Depends(admin_access)):
    try:
        member = await service.get_by_id(Id, session)
        if member:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(member))
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Member with {Id} ID not found")
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(ex)})

@member_router.post("/add")
async def add(memebr_data:AddUpdateMember, session:AsyncSession = Depends(get_session), 
            user_dtails = Depends(access_token_bearer),
            admin = Depends(admin_access)):
    try:
        new_member = await service.add(memebr_data, session)
        if new_member:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_member))
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=f"Faild to add member")
    except Exception as ex:
        return JSONResponse(status_code=500, content={"message": str(ex)})  

@member_router.post("/login")
async def login(login_data:Login, session:AsyncSession = Depends(get_session)):
    try:
        member = await service.get_member_by_username(login_data.username, session)
        if member is not None:
            valid_password = verfiy_password(login_data.password, member.Password) 
            if valid_password:
                data = {
                    "member_id": member.memebr_id,
                    "firstName": member.FirstName,
                    "lastName": member.LastName,
                    "phone_number": member.PhoneNumber,
                    "membership": member.membership_id,
                    "username": member.UserName,
                }
                token = create_token(data)
                data['token'] = token

                return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
            else:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid Username or Password")
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Invalid Username or Password")
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(ex)})

@member_router.put("/update/{Id}")
async def update(Id:int, memebr_data:AddUpdateMember, session:AsyncSession = Depends(get_session), 
            user_dtails = Depends(access_token_bearer),
            admin = Depends(admin_access)):
    try:
        updated_member = await service.update(Id, memebr_data, session)
        if updated_member:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(updated_member))
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Member with {Id} ID not found")
    except Exception as ex:
        return JSONResponse(status_code=500, content={"message": str(ex)})

@member_router.delete("/delete/{Id}")
async def delete(Id:int, session:AsyncSession = Depends(get_session), 
                user_dtails = Depends(access_token_bearer),
                admin = Depends(admin_access)):
    try:
        deleted_member = await service.delete(Id, session)
        if deleted_member:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(deleted_member))
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with {Id} ID not found")
    except Exception as ex:
        return JSONResponse(status_code=500, content={"message": str(ex)})

@member_router.get("/currentmember")
async def get_current_member(token: str = Depends(access_token_bearer), session = Depends(get_session)):
    try:
        data = await service.get_current_user(session=session, token=token)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(ex)})
    