from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import getcourse_api

app = FastAPI()


class Deal(BaseModel):
    deal_id: int
    offer_code: str
    product_title: str
    deal_cost: int
    user_email: str


@app.get("/{user_name}/deals")
def get_deals(user_name: str, status: Optional[str] = 'new'):
    response = getcourse_api.get_deals(user_name, getcourse_api.secret_key, status)
    return response


@app.post("/{user_name}/deals")
def post_deals(user_name, deal:Deal):
    params = {
        "user": {
            "email": deal.user_email,
        },
        "deal": {
            "product_title": deal.product_title,
            "deal_cost": deal.deal_cost,
            'deal_id': deal.deal_id,
        },
        "system": {
            "refresh_if_exists": 1,
        }
    }

    response = getcourse_api.post_deal(user_name, getcourse_api.secret_key, params)
    return response
