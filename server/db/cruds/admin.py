from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

from ..models import Admin


async def register_admin(session: AsyncSession, admin_login: str, password: str, who_create: str = None,
                         is_super_admin: bool = False, is_active: bool = True):
    admin_hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_admin = Admin(admin_login=admin_login, admin_hash_password=admin_hash_password, is_super_admin=is_super_admin,
                      is_active=is_active, who_create=who_create)

    session.add(new_admin)
    await session.commit()
    return new_admin


async def get_admin_login(session: AsyncSession, admin_login: str):
    admin = await session.execute(select(Admin).where(Admin.admin_login == admin_login))
    return admin.scalars().first()


async def get_admin_id(session: AsyncSession, admin_id: int):
    admin = await session.execute(select(Admin).where(Admin.id == admin_id))
    return admin.scalars().one()


async def set_active(session: AsyncSession, admin_id: int, is_active: bool):
    admin: Admin = await get_admin_id(session, admin_id)
    admin.is_active = is_active

    await session.commit()
    return admin


async def set_active_for_admin(session: AsyncSession, admin,  is_active: bool):
    admin.is_active = is_active

    await session.commit()
    return admin


async def delete_admin_for_admin(session: AsyncSession, admin):
    # print(admin)
    # admin.delete()
    await session.delete(admin)
    await session.commit()
    return "ok"
