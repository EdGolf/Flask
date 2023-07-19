import random
from fastapi import APIRouter, HTTPException, status, Depends
from db import init_db, OrderStatus, users, goods, orders
from user import pwd_context
from db import database
import datetime
from decimal import Decimal

service_router = APIRouter()


@service_router.get("/init-db")
async def init_database():
    init_db()

    users_list = [
        {
            "firstname": f"user{i}",
            "lastname": f"user{i}_last",
            "email": f"user{i}@mail.com",
            "password": pwd_context.hash(f"password{i}")
        } for i in range(5)]

    query = users.insert()
    await database.execute_many(query=query, values=users_list)
    query = users.select()
    users_from_db = await database.fetch_all(query=query)

    goods_list = [
        {
            "name": f"good{i}",
            "description": f"goog{i} description",
            "price": Decimal(round(random.random() * 100, 2))
        }
        for i in range(10)
    ]
    query = goods.insert()
    await database.execute_many(query=query, values=goods_list)
    query = goods.select()
    goods_from_db = await database.fetch_all(query=query)

    query = orders.insert()
    for _ in range(50):
        await database.execute(query=query, values={
            "datetime_create": datetime.datetime.now(),
            "user_id": random.choice(users_from_db).id,
            "good_id": random.choice(goods_from_db).id,
            "status": random.choice(list(OrderStatus))
        })

    return "db created"