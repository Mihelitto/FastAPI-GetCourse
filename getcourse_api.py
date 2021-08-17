import time
import json
import base64
import requests
from environs import Env


env = Env()
env.read_env()

account_name = "mihelitto"
secret_key = env.str('SECRET_KEY', 'REPLACE_ME')

params = {
    "user": {
        "email": "Test@test.com",
        "user_id": 189328860
    },
    "deal": {
        "product_title": "Тестовое предложение",
        "deal_cost": 3000,
        'deal_id': 120519562,
    },
    "system": {
        "refresh_if_exists": 1,
    }
}

def get_deals(account_name, secret_key, status):
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


def post_deal(account_name, secret_key, params):
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
