from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from ..database import get_async_session
from .models import task

from .schemas import TaskModel


router = APIRouter(
    prefix = "/tasks",
    tags=["Tasks"]
)


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(task)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_task(new_task: TaskModel, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(task).values(**new_task.dict())
        await session.execute(query)
        await session.commit()
        return {
            "status": "success",
            "task added !": task
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add task")


@router.put("/", response_model=TaskModel)
async def update_task(task_id: int, task_name: str = Query(None), description: str = Query(None),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(task).where(task.c.id == task_id).values(task_name=task_name,
                                                                description=description)
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "message": "Task up to date !",
            "Update task": task
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Task is not found")

@router.delete("/", response_model=TaskModel)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(task).where(task.c.id == task_id)
        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "message": "Task deleted successfully !"
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Task not found")
    