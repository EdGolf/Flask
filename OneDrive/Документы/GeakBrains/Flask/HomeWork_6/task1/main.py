from fastapi import FastAPI
from user import user_router
from good import good_router
from order import order_router
from services import service_router
from db import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(service_router, tags=["Service"])
app.include_router(user_router, tags=["User"])
app.include_router(good_router, tags=["Good"])
app.include_router(order_router, tags=["Order"])