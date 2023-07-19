from fastapi import APIRouter, HTTPException, status
from models import GoodIn, GoodOut, GoodUpdate
from db import database, goods

good_router = APIRouter()


@good_router.get("/goods", summary="Get all goods", response_model=list[GoodOut])
async def get_all_goods():
    query = goods.select()
    return await database.fetch_all(query)


@good_router.get("/goods/{good_id}", summary="Get good by id", response_model=GoodOut)
async def get_good(good_id: int):
    query = goods.select().where(goods.c.id == good_id)
    good = await database.fetch_one(query)
    if not good:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return good


@good_router.post("/goods", summary="Create new good", response_model=GoodOut)
async def create_good(new_good: GoodIn):
    query = goods.insert().values(**new_good.dict())
    last_record_id = await database.execute(query)
    query = goods.select().where(goods.c.id == last_record_id)
    return await database.fetch_one(query)


@good_router.put("/goods/{good_id}", summary="Update good", response_model=GoodOut)
async def update_good(good_id: int, update_good_data: GoodUpdate):
    update_data = {k: v for k, v in update_good_data.dict().items() if v is not None}
    query = goods.update().where(goods.c.id == good_id).values(**update_data)
    await database.execute(query)
    query = goods.select().where(goods.c.id == good_id)
    return await database.fetch_one(query)


@good_router.delete("/goods/{good_id}", summary="Delete good")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    await database.execute(query)
    return {'message': 'Good deleted'}