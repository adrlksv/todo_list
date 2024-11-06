from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users

from src.auth.schemas import UserRead, UserCreate

from src.tasks.router import router as task_router


app = FastAPI(
    title="Tasks"
)


@app.get("/")
async def enter():
    return {
        "message": "Your to do list !"
    }


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(task_router)
