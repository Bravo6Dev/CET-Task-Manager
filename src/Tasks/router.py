from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi import status, Depends

from src.Tasks.service import TaskService
from src.Tasks.base_model import AddTask

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db_context import get_session

from src.auth.dependencies import AccessTokenBearer, RolesChecker

task_router = APIRouter(prefix="/Tasks", tags=["Tasks"])
service = TaskService()
access_token_bearer = AccessTokenBearer()


@task_router.get("/getall")
async def get_all(session :AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.get_all(session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@task_router.get("/get/{Id}")
async def get_by_id(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.get_by_id(Id, session)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@task_router.post("/add")
async def add(task_data:AddTask, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        new_task = await service.add(task_data, session)
        if new_task is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=f"Faild to add task")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_task))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@task_router.put("/update/{Id}")
async def update(Id:int, task_data:AddTask, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        updated_task = await service.update(Id, task_data, session)
        if updated_task is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=f"Task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(updated_task))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@task_router.delete("/delete/{Id}")
async def delete(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        deleted_task = await service.delete(Id, session)
        if deleted_task is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f"Task with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(deleted_task))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))