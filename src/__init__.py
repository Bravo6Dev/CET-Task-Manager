from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.db.db_context import init_db

import uvicorn

from src.Members.routers import member_router
from src.MemberShip.routers import membership_router
from src.Projects.routers import project_router
from src.Tasks.router import task_router
from src.members_in_tasks.router import member_in_task_router

@asynccontextmanager
async def life_span(app:FastAPI):
    await init_db()
    yield

app = FastAPI(
    version="0.1",
    title="CET-TaskManager",
    lifespan=life_span
)

app.include_router(member_router )
app.include_router(membership_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(member_in_task_router)
