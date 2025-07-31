import httpx
import config

def create_invoice(user_id):
    url = "https://api.cryptomus.com/v1/payment"
    payload = {
        "amount": "10",
        "currency": "USDT",
        "order_id": str(user_id),
        "url_callback": f"{config.BASE_URL}/payment-callback"
    }
    headers = {
        "merchant": config.CRYPTOMUS_SHOP_ID,
        "sign": "",
        "Content-Type": "application/json",
        "api-key": config.CRYPTOMUS_API_KEY
    }

    response = httpx.post(url, json=payload, headers=headers)
    data = response.json()
    return data["result"]["url"]

