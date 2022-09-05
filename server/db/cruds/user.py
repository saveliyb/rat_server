import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import *

import datetime


async def register_victim(session: AsyncSession, pc_name: str, unique_number: int):
    new_victim = Victim(pc_name=pc_name, unique_number=unique_number, last_login_date=datetime.datetime.now())
    session.add(new_victim)
    await session.commit()
    return new_victim


async def get_victim_id(session: AsyncSession, victim_id: int):
    victim = await session.execute(select(Victim).where(Victim.id == victim_id))
    return victim.scalars().first()


async def get_victim_unique_number(session: AsyncSession, unique_number: int):
    victim = await session.execute(select(Victim).where(Victim.unique_number == unique_number))
    return victim.scalars().first()


async def get_active_victims(session: AsyncSession):
    time_now = time.time() - 15 * 60
    victims = await session.execute(select(Victim).where(Victim.last_login_time > time_now))
    return victims.scalars().all()
