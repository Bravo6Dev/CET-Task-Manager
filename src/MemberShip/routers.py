from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from MemberShip.service import MemberShipService
from db.db_context import get_session
from MemberShip.schema import AddUpdateMemberShip

from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import AccessTokenBearer, RolesChecker

membership_router = APIRouter(prefix="/MemberShip", tags=["MemberShip"])
membership_service = MemberShipService()
access_token_bearer = AccessTokenBearer()

@membership_router.get("/getall")
async def get_all(session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await membership_service.get_all(session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Message": str(ex)})

@membership_router.get("/get/{Id}")
async def get_by_id(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        memebrship = await membership_service.get_by_id(Id, session)
        if memebrship:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(memebrship))
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"Message": f"Membership with {Id} ID not found"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Message": str(ex)})

@membership_router.post("/add")
async def add(memebrship_data:AddUpdateMemberShip, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        membership = await membership_service.add(memebrship_data, session)
        if membership:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(membership))
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Message": f"Faild to add new membership"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Message": str(ex)})

@membership_router.put("/update/{Id}")
async def update(Id:int, memebrship_data:AddUpdateMemberShip, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        membership = await membership_service.update(Id, memebrship_data, session)
        if membership:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(membership))
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Message": f"Membership with {Id} ID not found"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Message": str(ex)})

@membership_router.delete("/delete/{Id}")
async def delete(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        membership = await membership_service.delete(Id, session)
        if membership:
            return JSONResponse(status_code=status.HTTP_200_OK, content=membership)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Message": f"Membership with {Id} ID not found"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Message": str(ex)})