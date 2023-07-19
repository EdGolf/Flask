from fastapi import APIRouter, HTTPException, status
from models import TaskIn, TaskOut, TaskUpdate
from db import tasks
from bson.objectid import ObjectId

task_router = APIRouter()


@task_router.get("/tasks", summary="Get all tasks", response_model=list[TaskOut])
async def get_all_tasks():
    result = [task for task in tasks.find()]
    for task in result:
        task['id'] = str(task['_id'])
    return result


@task_router.get("/tasks/{task_id}", summary="Get task by id", response_model=TaskOut)
async def get_task(task_id: str):
    task = tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        task['id'] = str(task['_id'])
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@task_router.post("/tasks", summary="Create new task", response_model=TaskOut)
async def create_task(new_task: TaskIn):
    result = tasks.insert_one(new_task.dict(exclude_none=True))
    new_task = tasks.find_one({'_id': result.inserted_id})
    new_task['id'] = str(new_task['_id'])
    return new_task


@task_router.put("/tasks/{task_id}", summary="Update task", response_model=TaskOut)
async def update_task(task_id: str, update_task_data: TaskUpdate):
    new_values = {k: v for k, v in update_task_data.dict().items() if v is not None}
    update_result = tasks.update_one({'_id': ObjectId(task_id)}, {'$set': new_values})
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    task = tasks.find_one({'_id': ObjectId(task_id)})
    task['id'] = str(task['_id'])
    return task


@task_router.delete("/tasks/{task_id}", summary="Delete task")
async def delete_task(task_id: str):
    delete_result = tasks.delete_one({'_id': ObjectId(task_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")