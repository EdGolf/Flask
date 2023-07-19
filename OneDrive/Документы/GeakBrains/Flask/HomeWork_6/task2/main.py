from fastapi import FastAPI
from task import task_router

app = FastAPI()

app.include_router(task_router, tags=["Task"])