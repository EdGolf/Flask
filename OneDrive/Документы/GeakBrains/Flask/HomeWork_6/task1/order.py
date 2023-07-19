from fastapi import APIRouter, HTTPException, status
from models import OrderIn, OrderOut, OrderUpdate, UserOut, GoodOut, UserOrderOut, OrderOutByUser
from db import database, orders, users, goods
from sqlalchemy import select, alias

order_router = APIRouter()


async def get_order_data(order_id: int) -> OrderOut | None:
    query = select([orders.c.id, orders.c.datetime_create, orders.c.status,
                    users.c.id.label("user_id"), users.c.firstname, users.c.lastname, users.c.email,
                    goods.c.id.label("good_id"), goods.c.name, goods.c.description, goods.c.price]). \
        join(users, orders.c.user_id == users.c.id). \
        join(goods, orders.c.good_id == goods.c.id). \
        where(orders.c.id == order_id)
    # query = f'''
    #     SELECT orders.id, orders.datetime_create, orders.status, users.id AS user_id, users.firstname,
    #            users.lastname, users.email, goods.id AS good_id, goods.name, goods.description, goods.price
    #     FROM orders
    #     JOIN users ON orders.user_id = users.id
    #     JOIN goods ON orders.good_id = goods.id
    #     WHERE orders.id = {order_id}
    # '''
    order = await database.fetch_one(query)
    if order:
        return OrderOut(id=order.id,
                        datetime_create=order.datetime_create,
                        status=order.status,
                        user=UserOut(id=order.user_id, firstname=order.firstname,
                                     lastname=order.lastname, email=order.email),
                        good=GoodOut(id=order.good_id, name=order.name,
                                     description=order.description, price=order.price))
    return None


@order_router.get("/orders", summary="Get all orders", response_model=list[OrderOut])
async def get_all_orders():
    query = select([orders.c.id, orders.c.datetime_create, orders.c.status,
                    users.c.id.label("user_id"), users.c.firstname, users.c.lastname, users.c.email,
                    goods.c.id.label("good_id"), goods.c.name, goods.c.description, goods.c.price]). \
        join(users, orders.c.user_id == users.c.id). \
        join(goods, orders.c.good_id == goods.c.id)
    # query = '''
    #     SELECT orders.id, orders.datetime_create, orders.status, users.id AS user_id, users.firstname,
    #            users.lastname, users.email, goods.id AS good_id, goods.name, goods.description, goods.price
    #     FROM orders
    #     JOIN users ON orders.user_id = users.id
    #     JOIN goods ON orders.good_id = goods.id
    # '''
    rows = await database.fetch_all(query)
    result = [OrderOut(id=row.id,
                       datetime_create=row.datetime_create,
                       status=row.status,
                       user=UserOut(id=row.user_id, firstname=row.firstname, lastname=row.lastname, email=row.email),
                       good=GoodOut(id=row.good_id, name=row.name, description=row.description, price=row.price))
              for row in rows]
    return result


@order_router.get("/orders/{order_id}", summary="Get order by id", response_model=OrderOut)
async def get_order(order_id: int):
    order = await get_order_data(order_id)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


@order_router.get("/orders/byuser/{user_id}", summary="Get order by user", response_model=UserOrderOut)
async def get_users_order(user_id: int):
    query = f'''
        SELECT orders.id, orders.datetime_create, orders.status, users.id AS user_id, users.firstname,
               users.lastname, users.email, goods.id AS good_id, goods.name, goods.description, goods.price
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN goods ON orders.good_id = goods.id
        WHERE users.id = {user_id}
    '''
    rows = await database.fetch_all(query)
    result = UserOrderOut(id=rows[0].user_id,
                          firstname=rows[0].firstname,
                          lastname=rows[0].lastname,
                          email=rows[0].email,
                          orders=[OrderOutByUser(id=row.id,
                                                 datetime_create=row.datetime_create,
                                                 status=row.status,
                                                 good=GoodOut(id=row.good_id,
                                                              name=row.name,
                                                              description=row.description,
                                                              price=row.price))
                                  for row in rows])
    return result


@order_router.post("/orders", summary="Create new order", response_model=OrderOut)
async def create_order(new_order: OrderIn):
    query = orders.insert().values(**new_order.dict())
    last_record_id = await database.execute(query)

    order = await get_order_data(last_record_id)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Error")


@order_router.put("/orders/{order_id}", summary="Update order", response_model=OrderOut)
async def update_order(order_id: int, update_order_data: OrderUpdate):
    update_data = {k: v for k, v in update_order_data.dict().items() if v is not None}
    query = orders.update().where(orders.c.id == order_id).values(**update_data)
    await database.execute(query)

    order = await get_order_data(order_id)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Error")


@order_router.delete("/orders/{order_id}", summary="Delete order")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}