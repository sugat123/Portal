from django.http import JsonResponse
import requests
from django.core import serializers
import json


def verification(url, token, amount):
    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount
    }
    headers = {
        "Authorization": "Key test_secret_key_e12fdbb02fd94fe4ab7440da6af6ca87"
    }

    response = requests.post(url, payload, headers=headers).json()

    return response


def transaction_list(url):
    url = url
    headers = {
        "Authorization": "Key test_secret_key_e12fdbb02fd94fe4ab7440da6af6ca87"
    }
    response = requests.get(url, {}, headers=headers).json()
    

    return response
