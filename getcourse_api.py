import time
import json
import base64
import requests
from typing import Optional
from config import secret_key
from models import Deal


def get_deals(account_name:str, status: Optional[str] = 'new'):
    export_deals_url = f"https://{account_name}.getcourse.ru/pl/api/account/deals"
    export_url = f"https://{account_name}.getcourse.ru/pl/api/account/exports/"
    export_deals_params = {'key': secret_key, 'status': status}
    params_export = {'key': secret_key}
    try:
        response = requests.get(export_deals_url, params=export_deals_params)
    except:
        print("Ошибка при обращении к серверу.")
        return {"error": True}
    request_deals = response.json()
    if request_deals['success']:
        export_id = request_deals['info']['export_id']

    while True:
        time.sleep(0.1)
        try:
            response = requests.get(export_url + str(export_id), params=params_export)
        except:
            print("Ошибка при обращении к серверу.")
            return {"error": True}
        request_deals
        if response.json()['success']:
            return response.json()


def post_deal(account_name: str, deal: Deal):
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

    import_deals_url = f"https://{account_name}.getcourse.ru/pl/api/deals"
    json_params = json.dumps(params)
    encode_params = base64.b64encode(json_params.encode("UTF-8"))
    params_import = {'action': 'add', 'key': secret_key, "params": encode_params}
    print(params_import)
    try:
        print("start")
        response = requests.post(import_deals_url, data=params_import)

    except:
        print("Ошибка при обращении к серверу.")
        return {"error": True}

    return response.json()
