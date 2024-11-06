from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from ..database import get_async_session
from src.models.models import Task

from .schemas import TaskModel


router = APIRouter(
    prefix = "/tasks",
    tags=["Tasks"]
)


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        return [TaskModel.from_orm(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")


@router.post("/", response_model=TaskModel)
async def add_task(new_task: TaskModel, session: AsyncSession = Depends(get_async_session)):
    try:
        task = Task(**new_task.dict())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return TaskModel.from_orm(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add task: {str(e)}")


@router.put("/{task_id}")
async def update_task(task_id: int, task_name: str = Query(None), description: str = Query(None),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        current_task = await session.get(Task, task_id)

        if current_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task_name is not None:
            current_task.task_name = task_name
        if description is not None:
            current_task.description = description

        await session.commit()
        await session.refresh(current_task)

        return TaskModel.from_orm(current_task)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update task")

@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        current_task = await session.get(Task, task_id)

        if current_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await session.delete(current_task)
        await session.commit()

        return {
            "status": "success",
            "message": "Task deleted successful !"
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete task")
