from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_context import get_session

from src.members_in_tasks.service import MemberInTaskService
from src.members_in_tasks.base_model import AddUpdateMemberInTask

from src.auth.dependencies import AccessTokenBearer, RolesChecker

member_in_task_router = APIRouter(prefix="/MembersInTasks", tags=["MembersInTasks"])
service = MemberInTaskService()
access_token_bearer = AccessTokenBearer()

@member_in_task_router.get("/getall")
async def get_all(session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.get_all(session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@member_in_task_router.get("/get/{Id}")
async def get_by_id(Id:int, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.get_by_id(Id, session)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Member in task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@member_in_task_router.post("/add")
async def add(member_in_task_data: AddUpdateMemberInTask, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.add(member_in_task_data, session)
        if data is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=f"Faild to add member in task")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


@member_in_task_router.put("/update/{Id}")
async def update(Id:int, member_in_task_data: AddUpdateMemberInTask, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.update(Id, member_in_task_data, session)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Member in task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@member_in_task_router.delete("/delete/{Id}")
async def delete(Id:int, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.delete(Id, session)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Member In task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
