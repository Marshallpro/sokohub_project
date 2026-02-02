import uuid
import requests
from django.conf import settings

MOMO_BASE_URL = "https://sandbox.momodeveloper.mtn.com"

def momo_request_to_pay(amount, phone, reference):
    url = f"{MOMO_BASE_URL}/collection/v1_0/requesttopay"

    headers = {
        "X-Reference-Id": reference,
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.MOMO_ACCESS_TOKEN}",
    }

    payload = {
        "amount": str(amount),
        "currency": "RWF",
        "externalId": reference,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone,
        },
        "payerMessage": "SokoHub Order Payment",
        "payeeNote": "Thank you for shopping",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code
