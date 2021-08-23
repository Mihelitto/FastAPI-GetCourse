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
    secret_key: str
