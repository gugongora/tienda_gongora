import requests
from .webpay_conf import WEBPAY_API_BASE_URL, WEBPAY_API_KEY_ID, WEBPAY_API_KEY_SECRET

def crear_transaccion(session_id, amount, buy_order, return_url):
    url = f"{WEBPAY_API_BASE_URL}/transactions"

    headers = {
        "Tbk-Api-Key-Id": WEBPAY_API_KEY_ID,
        "Tbk-Api-Key-Secret": WEBPAY_API_KEY_SECRET,
        "Content-Type": "application/json",
    }

    data = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": float(amount),
        "return_url": return_url,
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Lanza excepción si falla
    
    return response.json()       # Devuelve dict con 'token' y 'url'
