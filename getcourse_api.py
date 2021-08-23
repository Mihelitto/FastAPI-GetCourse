import time
import json
import base64
from json import JSONDecodeError
import requests
from fastapi import Depends
from typing import Optional
from models import Deal
from authentication import get_current_user


def get_deals(status: Optional[str] = 'new', user: tuple = Depends(get_current_user)):
    account_name = user[1]
    export_deals_url = f"https://{account_name}.getcourse.ru/pl/api/account/deals"
    export_url = f"https://{account_name}.getcourse.ru/pl/api/account/exports/"
    export_deals_params = {'key': user[2], 'status': status}
    params_export = {'key': user[2]}

    try:
        response = requests.get(export_deals_url, params=export_deals_params)
        request_deals = response.json()
    except JSONDecodeError:
        print("Ошибка при обращении к серверу.")
        return {"error": response.text}
    except:
        print("Ошибка при обращении к серверу.")
        return {"error": True}

    if request_deals['success']:
        export_id = request_deals['info']['export_id']
    else:
        return {"error": True, "message": request_deals["error_message"]}

    while True:
        time.sleep(0.5)
        try:
            response = requests.get(
                export_url + str(export_id),
                params=params_export
            )
        except:
            print("Ошибка при обращении к серверу.")
            return {"error": True}
        request_deals
        if response.json()['success']:
            return response.json()


def post_deal(deal: Deal, user: tuple = Depends(get_current_user)):
    account_name = user[1]
    params = {
        "user": {
            "email": deal.user_email,
        },
        "deal": {
            "product_title": deal.product_title,
            "offer_code": deal.offer_code,
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
    params_import = {'action': 'add', 'key': user[2], "params": encode_params}

    try:
        response = requests.post(import_deals_url, data=params_import)
        deals = response.json()
    except JSONDecodeError:
        print("Ошибка при обращении к серверу.")
        return {"error": response.text}
    except:
        print("Ошибка при обращении к серверу.")
        return {"error": True}

    return deals
