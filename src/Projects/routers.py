from Projects.service import ProjectService
from Projects.base_model import AddUpdateProject

from fastapi.routing import APIRouter
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder   
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession 
from db.db_context import get_session

from auth.dependencies import AccessTokenBearer, RolesChecker

project_router = APIRouter(prefix="/Projects", tags=["Projects"])
service = ProjectService()
access_token_bearer = AccessTokenBearer()    


@project_router.get("/getall")
async def get_all(session :AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        data = await service.get_all(session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@project_router.get("/get/{Id}")
async def get_by_id(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        project = await service.get_by_id(Id, session)
        if project is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(project))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@project_router.post("/add")
async def add(memebr_data:AddUpdateProject, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        if memebr_data is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Faild to add new project")
        new_project = await service.add(memebr_data, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_project))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@project_router.put("/update/{Id}")
async def update(Id:int, memebr_data:AddUpdateProject, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        updated_project = await service.update(Id, memebr_data, session)
        if updated_project is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Project with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(updated_project))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@project_router.delete("/delete/{Id}")
async def delete(Id:int, session:AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)):
    try:
        deleted_project = await service.delete(Id, session)
        if deleted_project is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Project with {Id} ID not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(deleted_project))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))