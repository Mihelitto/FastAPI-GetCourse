from typing import Optional
from pydantic import BaseModel


class Deal(BaseModel):
    deal_id: Optional[int] = None
    offer_code: Optional[str] = None
    product_title: Optional[str] = None
    deal_cost: int
    user_email: str


class NewUser(BaseModel):
    username: str
    password: str
    password_repeat: str
    secret_key: str
