import os 
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram import Bot, Dispatcher, Router
from app.db.database import Database
from aiogram.fsm.state import State, StatesGroup


# Загружаем переменные из .env
load_dotenv("/Users/masterpo/Desktop/TheThinker/backend/.env")

class Settings():
    # Stickers
    ST0 = os.getenv("sticker0")
    ST1 = os.getenv("sticker1")
    ST2 = os.getenv("sticker2")
    ST3 = os.getenv("sticker3") 
    sticker_pack = [ST0, ST1, ST2, ST3]

    # Wallets
    ETH_WALLET = os.getenv("ETH_WALLET")
    TRON_WALLET = os.getenv("TRON_WALLET")
    TON_WALLET = os.getenv("TON_WALLET")

    # API keys
    API_TRON_KEY = os.getenv("API_TRON_KEY")
    API_TON_KEY = os.getenv("API_TON_KEY")
    API_URL = os.getenv("API_URL")

    TON_USDT_KEY = os.getenv("TON_USDT_KEY")

    # Telegram bot API
    LINK = os.getenv("LINK")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    WITHDRAW_GROUP_ID = os.getenv("WITHDRAW_GROUP_ID")
    GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # TON address regex
    TON_ADDRESS_REGEX = os.getenv("TON_ADDRESS_REGEX")

    USDT_CONTRACT = os.getenv("USDT_CONTRACT")

settings = Settings()
