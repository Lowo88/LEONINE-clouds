# pet.py

import os
import requests
import time
import logging
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()  # Load environment variables from .env file

# Set up logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Pet:
    def __init__(self, name, pet_type):
        self.name = name
        self.pet_type = pet_type
        self.is_alive = True  # Pet alive status

    def talk(self, message):
        """Pet can talk to the user."""
        return f"{self.name} says: {message}"

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

    def place_limit_order(self, side, amount, price):
        """Place a limit order to buy or sell ZEC."""
        url = f"{self.base_url}/orders"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "type": "limit",
            "side": side,
            "product_id": "ZEC-USD",
            "price": price,
            "size": amount
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error placing order: {response.status_code} - {response.text}")

class Wallet:
    def __init__(self):
        self.zec_balance = 10.0  # Initial balance of 10 ZEC

    def deposit(self, amount):
        """Deposit ZEC into the wallet."""
        self.zec_balance += amount

    def withdraw(self, amount):
        """Withdraw ZEC from the wallet."""
        if amount <= self.zec_balance:
            self.zec_balance -= amount
            return amount
        else:
            raise Exception("Insufficient balance in the wallet.")

    def get_balance(self):
        """Get the current ZEC balance in the wallet."""
        return self.zec_balance

class VirtualPetTradingBot:
    def __init__(self, pet_name, pet_type):
        self.pet = Pet(pet_name, pet_type)
        self.coinbase_api = CoinbaseAPI()
        self.wallet = Wallet()
        self.price_history = []  # To store price history for trading strategies

    def send_notification(self, subject, message):
        """Send an email notification."""
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    def calculate_sma(self, period):
        """Calculate the Simple Moving Average (SMA)."""
        if len(self.price_history) < period:
            return None
        return sum(self.price_history[-period:]) / period

    def trade(self):
        """Simulate trading based on user input and market conditions."""
        while self.pet.is_alive:
            try:
                zec_price = self.coinbase_api.get_zec_price()
                self.price_history.append(zec_price)
                logging.info(f"Current ZEC Price: ${zec_price}")

                # Check for significant price changes
                if len(self.price_history) > 1:
                    price_change = (zec_price - self.price_history[-2]) / self.price_history[-2] * 100
                    if abs(price_change) >= 5:  # Notify if price changes by 5% or more
                        self.send_notification("Significant Price Change", f"ZEC price changed by {price_change:.2f}% to ${zec_price}")

                # Implement a simple trading strategy based on SMA
                sma = self.calculate_sma(5)  # Calculate 5-period SMA
                if sma:
                    if zec_price < sma:  # Buy signal
                        amount_to_buy = 1  # Example amount
                        limit_price = zec_price * 0.98  # Buy at 2% below current price
                        order_response = self.coinbase_api.place_limit_order("buy", amount_to_buy, limit_price)
                        logging.info(f"Buy Order Response: {order_response}")
                        self.wallet.deposit(amount_to_buy)  # Update wallet balance
                        self.send_notification("Trade Executed", f"Bought {amount_to_buy} ZEC at ${limit_price:.2f}")

                    elif zec_price > sma:  # Sell signal
                        amount_to_sell = 1  # Example amount
                        limit_price = zec_price * 1.02  # Sell at 2% above current price
                        order_response = self.coinbase_api.place_limit_order("sell", amount_to_sell, limit_price)
                        logging.info(f"Sell Order Response: {order_response}")
                        self.wallet.withdraw(amount_to_sell)  # Update wallet balance
                        self.send_notification("Trade Executed", f"Sold {amount_to_sell} ZEC at ${limit_price:.2f}")

                # User interaction for manual commands
                user_input = input("Enter 'check wallet' or 'ask pet': ").strip().lower()
                if user_input == "check wallet":
                    print(f"Current ZEC balance in wallet: {self.wallet.get_balance()} ZEC")
                elif user_input == "ask pet":
                    print(self.pet.talk("what's the price of zec?"))

                # Simulate time passing
                time.sleep(10)  # Wait for 10 seconds before the next interaction

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                break

# Example usage
if __name__ == "__main__":
    trading_bot = VirtualPetTradingBot("Zoe", "Zebra")
    trading_bot.trade()

    # - This method fetches the user's ZEC wallet address from their Coinbase account. It retrieves the account information and looks for the account associated with ZEC.
    
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

    def get_wallet_address(self):
        """Fetch the user's ZEC wallet address."""
        url = f"{self.base_url}/accounts"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            accounts = response.json()['data']
            for account in accounts:
                if account['currency'] == 'ZEC':
                    return account['id']  # Return the account ID or address
        else:
            raise Exception(f"Error fetching wallet address: {response.status_code} - {response.text}")

    def withdraw_zec(self, amount, address):
        """Withdraw ZEC to an external wallet address."""
        url = f"{self.base_url}/withdrawals"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "currency": "ZEC",
            "address": address
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error withdrawing ZEC: {response.status_code} - {response.text}")