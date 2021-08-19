from typing import Optional
from pydantic import BaseModel


class Deal(BaseModel):
    deal_id: int
    offer_code: str
    product_title: str
    deal_cost: int
    user_email: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
