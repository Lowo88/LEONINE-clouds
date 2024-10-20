# coinbase_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class CoinbaseAPI:
    def __init__(self):
        self.api_key = os.getenv("COINBASE_API_KEY")
        self.api_secret = os.getenv("COINBASE_API_SECRET")
        self.base_url = "https://api.coinbase.com/v2"

    def get_zec_price(self):
        """Fetch the current price of ZEC in USD."""
        url = f"{self.base_url}/prices/ZEC-USD/spot"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['amount'])
        else:
            raise Exception(f"Error fetching ZEC price: {response.status_code} - {response.text}")

    def buy_zec(self, amount_usd):
        """Buy ZEC with a specified amount in USD."""
        url = f"{self.base_url}/buys"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount_usd,
            "currency": "USD",
            "payment_method": "YOUR_PAYMENT_METHOD_ID"  # Replace with your payment method ID
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error buying ZEC: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    coinbase_api = CoinbaseAPI()

    try:
        zec_price = coinbase_api.get_zec_price()
        print(f"Current ZEC Price: ${zec_price}")

        # Example of buying ZEC
        amount_to_buy = 10  # Amount in USD
        purchase_response = coinbase_api.buy_zec(amount_to_buy)
        print("Purchase Response:", purchase_response)

    except Exception as e:
        print("An error occurred:", e)
        
