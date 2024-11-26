import logging
import base64
import requests
from aiogram import Bot, Dispatcher, types, Router

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database
from config import TOKEN, ProfileCreation, ETH_WALLET, sticker_pack
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import random
import re
from config import TON_WALLET, TON_ADDRESS_REGEX, API_TRON_KEY, API_TON_KEY, API_URL

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder  


net = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="TON", callback_data=('ton'))], 
                     [InlineKeyboardButton(text="TRC20", callback_data=('trc'))]])

done = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Done", callback_data=('done'))]])

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()
router = Router()

class Wallet(StatesGroup):
    address = State()
    net = State()
    user_id = State()
    random_float = State()
 



def change_format(wallet):
    u_wallet = wallet
    e_char = "E"
    e_wallet = e_char + u_wallet[1:]
    return e_wallet
    

# Проверка TRC20 адреса
def is_trc20_address(address: str) -> bool:
    pattern = r"^T[1-9A-HJ-NP-Za-km-z]{33}$"
    return bool(re.match(pattern, address))

def is_ton_address(address):
    if not re.match(TON_ADDRESS_REGEX, address):
        return False
    try:
        # Пробуем декодировать адрес в Base64
        decoded = base64.urlsafe_b64decode(address + '==')
        # Длина TON адреса должна быть равна 36 байтам
        if len(decoded) == 36:
            return True
        else:
            return False
    except (ValueError, base64.binascii.Error):
        # Ошибка декодирования
        return False

# Проверка транзакций пользователя
def get_ton_transactions(address, limit=10):
    if not is_ton_address(address):
        logging.error(f"Invalid TON address: {address}")
        return None

    endpoint = f'{API_URL}getTransactions'
    params = {
        'address': address,
        'limit': limit,
        'api_key': API_TON_KEY
    }

    # Отправляем запрос к API
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            return data.get('result', [])
        else:
            logging.error(f"API Error: {data.get('error')}")
    else:
        logging.error(f"HTTP Error: {response.status_code}")
    
    return None
# if is_ton_address(wallet) and verif == 1:
#         await message.answer("Where do you want to log in?", reply_markup=net)
#     if wallet 
#     await message.answer("Hello, this is LUF authorisation bot. Choose the net.", reply_markup=net)


# Проверка TRC20 адреса
def is_trc20_address(address: str) -> bool:
    pattern = r"^T[1-9A-HJ-NP-Za-km-z]{33}$"
    return bool(re.match(pattern, address))

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

def get_tron_transactions(tron_address, api_key):
    endpoint = f'https://apilist.tronscan.org/api/transaction?address={tron_address}&limit=20&sort=-timestamp'
    headers = {'TRON-PRO-API-KEY': api_key}

    try:
        response = requests.get(endpoint, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            data = response.json()
            if data.get('total') > 0 and data.get('data'):
                transactions = []
                for tx in data['data']:
                    amount = float(tx.get('amount', '0')) / 1e6
                    transactions.append({
                        'hash': tx.get('hash', 'Не указано'),
                        'sender': tx.get('ownerAddress', 'Не указано'),
                        'recipient': tx.get('toAddress', 'Не указано'),
                        'confirmed': tx.get('confirmed', 'Не указано'),
                        'amount': "{:.6f}".format(amount),
                        'timestamp': format_timestamp(tx.get('timestamp', 0))
                    })
                return transactions
    except Exception as e:
        logging.error(f"Произошла ошибка при запросе транзакций: {e}")
    return []

def get_tron_usdt_transactions(tron_address, api_key):
    usdt_contract_address = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
    endpoint = f'https://apilist.tronscan.org/api/contract/events?limit=20&contract={usdt_contract_address}&address={tron_address}&sort=-timestamp'
    headers = {'TRON-PRO-API-KEY': api_key}
    # print(2)
    try:
        # print(3)
        response = requests.get(endpoint, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            data = response.json()
            print(data)  # Добавьте эту строку для отладки
            if data.get('total') > 0 and data.get('data'):
                transactions = []
                # print(4)
                for tx in data['data']:
                    # print(5)
                    if tx.get('tokenName') == 'Tether USD':  # Проверяем, что это USDT
                        # print(6)
                        amount = float(tx.get('amount', '0')) / 1e6
                        transactions.append({
                            'hash': tx.get('transactionHash', 'Не указано'),
                            'sender': tx.get('transferFromAddress', 'Не указано'),
                            'recipient': tx.get('transferToAddress', 'Не указано'),
                            'confirmed': tx.get('confirmed', 'Не указано'),
                            'amount': "{:.6f}".format(amount),
                            'timestamp': format_timestamp(tx.get('timestamp', 0))
                        })
                return transactions
        else:
            logging.error(f"Ошибка запроса: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Произошла ошибка при запросе транзакций: {e}")
    return []
