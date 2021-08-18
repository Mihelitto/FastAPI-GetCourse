from typing import Optional
from fastapi import FastAPI, Depends
from models import Deal
import getcourse_api

app = FastAPI()


@app.get("/{account_name}/deals")
def get_deals(deals: dict = Depends(getcourse_api.get_deals)):
    return deals


@app.post("/{account_name}/deals")
def post_deals(deal: dict = Depends(getcourse_api.post_deal)):
    return deal
