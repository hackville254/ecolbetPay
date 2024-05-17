import requests
import json
from decouple import config

from .orderId import generate_random_alphanumeric
from .schemas import MySoleaPay
from ninja import Router
from ninja.errors import HttpError

router = Router()
BASE_URL = "https://soleaspay.com/api/"



@router.post('payin', tags=['PayIn Router'], auth=None)
def payinFunction(request, data: MySoleaPay):
    # Vérification de l'opérateur
    if data.operator not in [1, 2]:
        raise HttpError(
            status_code=400, message="Invalid operator. Must be 1 (OM) or 2 (MOMO).")

    url = f"{BASE_URL}agent/bills"
    headers = {
        "x-api-key": config('X-API-KEY'),
        "operation": str(data.operator),
        "service": "2",
        "Content-Type": "application/json"
    }
    order_id = generate_random_alphanumeric()
    data = {
        "wallet": data.customer_number,
        "amount": data.amount,
        "currency": "XAF",
        "order_id": order_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    result["ecolbet_id"] = order_id
    return result


@router.get('verify', tags=["CHECK TRANSACTION WITCH *ecolbet_id*"], auth=None)
def verifyTransaction(request, operator: str, amount: float, ecolbet_id: str, payToken: str):
    url = f"{BASE_URL}agent/verif-pay"
    headers = {
        "x-api-key": config('X-API-KEY'),
        "operation": str(operator),
        "service": "1",
        "Content-Type": "application/json"
    }
    params = {
        "amount": amount,
        "orderId": ecolbet_id,
        "payId": payToken
    }

    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    return result


@router.post('payOut', tags=["Send the money to the client"], auth=None)
def payOut(request, data: MySoleaPay):
    url = f"{BASE_URL}action/auth"
    if data.operator not in [1, 2]:
        raise HttpError(
            status_code=400, message="Invalid operator. Must be 1 (OM) or 2 (MOMO).")

    payload = {
        "public_apikey": config('X-API-KEY'),
        "private_secretkey": config('PRIVATE_SECRET_KEY'),
    }
    response = requests.request("POST", url, json=payload)

    response_data = json.loads(response.text)
    print(response_data['access_token'])
    if 'access_token' in response_data:
        url = f"{BASE_URL}user/proceeds"
        headers = {
            "operation": str(data.operator),
            "service": "1",
            "Authorization": "Bearer " + response_data['access_token'],
            "Content-Type": "application/json"
        }
        data = {
            "amount": data.amount,
            "wallet": data.customer_number
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        return result
