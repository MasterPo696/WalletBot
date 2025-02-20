import logging
import base64
import re
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any

from aiogram import Bot, Router, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from app.db.database import Database
from app.config import settings

class CryptoHandler:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Initialize bot components
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Database()
        self.router = Router()

    class Wallet(StatesGroup):
        """State machine for wallet operations"""
        address = State()
        net = State()
        user_id = State()
        random_float = State()

    def change_format(self, wallet: str) -> str:
        return f"E{wallet[1:]}"

    def is_trc20_address(self, address: str) -> bool:
        pattern = r"^T[1-9A-HJ-NP-Za-km-z]{33}$"
        return bool(re.match(pattern, address))

    def is_ton_address(self, address: str) -> bool:
        if not re.match(settings.TON_ADDRESS_REGEX, address):
            return False
            
        try:
            decoded = base64.urlsafe_b64decode(address + '==')
            return len(decoded) == 36
        except (ValueError, base64.binascii.Error):
            return False

    def get_ton_transactions(self, address: str, limit: int = 10) -> Optional[List[Dict]]:
        if not self.is_ton_address(address):
            self.logger.error(f"Invalid TON address: {address}")
            return None

        params = {
            'address': address,
            'limit': limit,
            'api_key': settings.API_TON_KEY
        }

        try:
            response = requests.get(f'{settings.API_URL}getTransactions', params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok'):
                return data.get('result', [])
            self.logger.error(f"API Error: {data.get('error')}")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
        
        return None

    def format_timestamp(self, timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def get_tron_transactions(self, tron_address: str, api_key: str) -> List[Dict[str, Any]]:
        endpoint = f'https://apilist.tronscan.org/api/transaction?address={tron_address}&limit=20&sort=-timestamp'
        headers = {'TRON-PRO-API-KEY': api_key}

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data.get('total', 0) > 0 and data.get('data'):
                return [
                    {
                        'hash': tx.get('hash', 'Not specified'),
                        'sender': tx.get('ownerAddress', 'Not specified'), 
                        'recipient': tx.get('toAddress', 'Not specified'),
                        'confirmed': tx.get('confirmed', 'Not specified'),
                        'amount': f"{float(tx.get('amount', '0')) / 1e6:.6f}",
                        'timestamp': self.format_timestamp(tx.get('timestamp', 0))
                    }
                    for tx in data['data']
                ]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch TRON transactions: {e}")
        
        return []

    def get_tron_usdt_transactions(self, tron_address: str, api_key: str) -> List[Dict[str, Any]]:
        usdt_contract = settings.USDT_CONTRACT
        endpoint = f'https://apilist.tronscan.org/api/contract/events'
        params = {
            'limit': 20,
            'contract': usdt_contract,
            'address': tron_address,
            'sort': '-timestamp'
        }
        headers = {'TRON-PRO-API-KEY': api_key}

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data.get('total', 0) > 0 and data.get('data'):
                transactions = []
                for tx in data['data']:
                    if tx.get('tokenName') == 'Tether USD':
                        transactions.append({
                            'hash': tx.get('transactionHash', 'Not specified'),
                            'sender': tx.get('transferFromAddress', 'Not specified'),
                            'recipient': tx.get('transferToAddress', 'Not specified'),
                            'confirmed': tx.get('confirmed', 'Not specified'),
                            'amount': f"{float(tx.get('amount', '0')) / 1e6:.6f}",
                            'timestamp': self.format_timestamp(tx.get('timestamp', 0))
                        })
                return transactions
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch USDT transactions: {e}")
            
        return []
