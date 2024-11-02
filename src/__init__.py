from fastapi import FastAPI

from contextlib import asynccontextmanager

from db.db_context import init_db

import uvicorn

from Members.routers import member_router
from MemberShip.routers import membership_router
from Projects.routers import project_router
from Tasks.router import task_router
from members_in_tasks.router import member_in_task_router

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

if __name__ == "__main__":
    uvicorn.run("__init__:app", host="127.0.0.1", port=8000, reload=True, lifespan='on')