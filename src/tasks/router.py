from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from ..database import get_async_session
from src.models.models import task

from .schemas import TaskModel


router = APIRouter(
    prefix = "/tasks",
    tags=["Tasks"]
)


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(task)
        result = await session.execute(query)
        tasks = result.all()

        return [TaskModel.from_orm(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")


@router.post("/")
async def add_task(new_task: TaskModel, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(task).values(**new_task.dict())

        await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "message": "task added successful !"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add task: {e}")
    

@router.put("/{task_id}")
async def update_task(task_id: int, task_name: str = Query(None), description: str = Query(None),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(task).where(task.c.id == task_id)
        result = await session.execute(query)
        current_task = result.scalar_one_or_none()

        if current_task is None:
            raise HTTPException(status_code=404, detail="Task is not found")
        
        update_values = {}
        
        if task_name:
            update_values["task_name"] = task_name
        if description:
            update_values["description"] = description
        
        update_query = update(task).where(task.c.id == task_id).values(**update_values)

        await session.execute(update_query)
        await session.commit()


        return {
            "status": "success",
            "message": "Task updated successful !"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task update failed: {e}")
    

@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(task).where(task.c.id == task_id)
        result = await session.execute(query)
        current_task = result.scalar_one_or_none()

        if current_task is None:
            raise HTTPException(status_code=404, detail="Task is not found")
        
        delete_query = delete(task).where(task.c.id == task_id)

        await session.execute(delete_query)
        await session.commit()

        return {
            "status": "success",
            "message": "Task deleted successful !"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deleted failed: {e}")
