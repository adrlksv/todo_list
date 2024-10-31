from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from database import get_async_session
from models import task

from schemas import TaskModel


router = APIRouter(
    prefix = "/tasks",
    tags=["Tasks"]
)


@router.get("/")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(task)
    result = await session.execute(query)
    return result.all()


# @router.post("/", response_model=TaskModel)
# async def add_tasks(task: TaskModel):
#     tasks.append(task)
#     return task


# @router.put("/{task_id}")
# async def update_task(task_id: int, task_name: str = Query(None), description: str = Query(None)):
#     try:
#         current_task = next((i for i, t in enumerate(tasks) if t.id == task_id), None)

#         if current_task is not None:
#             tasks[current_task].task_name = task_name
#             tasks[current_task].description = description
            
#             return tasks[current_task]
#         else:
#             raise HTTPException(status_code=404, detail="Task not found")
#     except Exception:
#         raise HTTPException(status_code=500, detail="Error updating task")


# @router.delete("/{task_id}")
# async def delete_task(task_id: int):
#     try:
#         current_task = next((i for i, t in enumerate(tasks) if t.id == task_id), None)

#         if current_task is not None:
#             del tasks[current_task]

#             return tasks
#         else:
#             raise HTTPException(status_code=404, detail="Task not found")
#     except Exception:
#         raise HTTPException(status_code=500, detail="Error deleting task")
