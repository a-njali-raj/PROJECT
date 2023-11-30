import requests
import json

from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from datetime import timedelta


def generate_order(amount):
    data = {
        "amount": int(amount * 100),
        "currency": "INR",
        "partial_payment": False,
    }
    response = requests.post(
        'https://api.razorpay.com/v1/orders/',
        headers={
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        print(f"Error generating Razorpay order: {response.status_code}, {response.content}")
        return None