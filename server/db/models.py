from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Float, Boolean

# from db_config import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            return session


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    admin_login = Column(String)
    admin_hash_password = Column(String)
    is_super_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    who_create = Column(String, default=None)


class Victim(Base):
    __tablename__ = "Victims"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    pc_name = Column(String)
    unique_number = Column(Integer)
    last_login_date = Column(DateTime)
    last_login_time = Column(Float)
