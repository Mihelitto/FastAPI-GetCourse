from pydantic import BaseModel


class Deal(BaseModel):
    deal_id: int
    offer_code: str
    product_title: str
    deal_cost: int
    user_email: str
