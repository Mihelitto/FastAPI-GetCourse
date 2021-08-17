from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Deal(BaseModel):
    deal_number: int
    offer_code: str
    product_title: str
    deal_cost: int
    user_email: str


@app.get("/{user_name}/deals")
def get_deals(user_name: str, status: Optional[str] = 'new'):
    return {"Name": user_name, "status": status}


@app.post("/{user_name}/deals")
def post_deals(deal:Deal):
    return deal
