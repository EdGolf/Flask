
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .models import UserIn, UserOut, UserPut

app = FastAPI()
templates = Jinja2Templates(directory="homework5/task1/templates")

users: dict[int, UserIn] = {i: UserIn(name=f'user{i}', email=f'email{i}@mail.com', password=f'password{i}')
                            for i in range(5)}


@app.post('/users', response_model=UserOut, tags=['Users'], summary="Add new user")
async def user_post(new_user: UserIn):
    new_user_id = max(users.keys()) + 1
    users[new_user_id] = new_user
    return UserOut(id=new_user_id, name=new_user.name, email=new_user.email)


@app.put('/users', response_model=UserOut, tags=['Users'], summary="Update users data by id")
async def user_put(user_id: int, user_new_data: UserPut):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not Found")

    user.name = user_new_data.name or user.name
    user.email = user_new_data.email or user.email
    user.password = user_new_data.password or user.password

    return UserOut(id=user_id, name=user.name, email=user.email)


@app.delete('/users', tags=['Users'], summary="Delete user by id")
async def user_delete(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Not Found")
    users.pop(user_id)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    users_list = [UserOut(id=k, name=v.name, email=v.email) for k, v in users.items()]
    return templates.TemplateResponse("users.html", {"request": request, "users": users_list, "title": "Пользователи"})