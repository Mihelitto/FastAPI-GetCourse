from typing import Optional
from pydantic import BaseModel


class Deal(BaseModel):
    deal_id: int
    offer_code: str
    product_title: str
    deal_cost: int
    user_email: str


class NewUser(BaseModel):
    username: str
    password: str
    password_repeat: str


class User(BaseModel):
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
