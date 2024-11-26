from aiogram import Bot, Dispatcher, types, F
from aiogram import Bot, Dispatcher, Router
from database import Database
from aiogram.fsm.state import State, StatesGroup

### Stickers for the animation.
sticker0 = "CAACAgQAAxkBAAIJUmbVXeF-yExM2Lvbr-n-rJFc83JBAAKfGQACKQ2oUtN9SrcNi7jdNQQ"
sticker1 = "CAACAgQAAxkBAAIJVGbVXeJZcgt9lG3-tLPhimGa3uBMAALLFAACI_CoUt9JFDV3tKp9NQQ"
sticker2 = "CAACAgQAAxkBAAIJWGbVXeO_LWCMlK7Ek3gk0Su8gE3gAALsGgAC8LepUhmqRg96ZVP1NQQ"
sticker3 = "CAACAgQAAxkBAAIJVmbVXeLAUXTQkFjZ3DPu9zOhovqfAAKbFAAC7_apUnu5-dj9jlATNQQ"
sticker_pack = [sticker0, sticker1, sticker2, sticker3]



### Your wallets.
ETH_WALLET = "YOUR_ETH_WALLET"                           
TRON_WALLET = "YOUR_TRON_WALLET"                        
TON_WALLET = 'YOUR_TON_WALLET'                          

### Your API keys to scan the nets.
API_TRON_KEY = 'APU_TRON_SCAN'
API_TON_KEY = 'API_TON_SCAN'
API_URL = 'https://toncenter.com/api/v2/'

### Links and your telegram bot IDs
LINK = "https://example.com"
TOKEN = "BOT_TOKEN"
CHANNEL_ID = 'CHANNEL_ID'
WITHDRAW_GROUP_ID = 'GROUP_FOR_LOGS'
GROUP_CHAT_ID = "@GROUP_CHAT_ID"

TON_ADDRESS_REGEX = r'^[-A-Za-z0-9_]{48}$'

TON_USDT_KEY = "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT" # defining key/request url 




db = Database()
bot = Bot(token=TOKEN)
dp = Dispatcher()
database = Database()
router = Router()
exp_router = Router()

class Wallet(StatesGroup):
    address = State()
    net = State()
    user_id = State()
    random_float = State()
    currency = State()