from fastapi import FastAPI

from src.tasks.router import router as task_router


app = FastAPI(
    title="Tasks"
)


@app.get("/")
async def enter():
    return {
        "message": "Your to do list !"
    }


app.include_router(task_router)
