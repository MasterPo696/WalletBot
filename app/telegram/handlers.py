import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from app.db.database import Database
from config import settings
from app.crypto.functions import CryptoHandler
from app.telegram.kb import kbrd
import asyncio
import random
import requests
from datetime import datetime

crypto = CryptoHandler()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()
router = Router()

class WalletStates(StatesGroup):
    action = State()
    amount_usdt = State()
    withdraw_usdt = State()
    currency = State()
    message = State()
    amount_ton = State()

wallet = crypto.Wallet()

@router.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    result = db.check_wallet(user_id)
    
    if result[0] and result[1]:
        await message.answer(f"Welcome back, {user_name}! All possible wallets are connected.")
    elif result[0]:
        await bot.send_sticker(user_id, settings.ST3)
        await message.answer(f"Hello, *{user_name}*\!\n\nThe *TON* is already connected\.\n\nPress *TRON to add TRC20*\.", parse_mode="MarkdownV2", reply_markup=kbrd.net)
        await message.answer("Please use DEX - (non costideal wallets) as TonKeeper, TrustWallet")
        await bot.send_sticker(user_id, settings.ST3)
        await message.answer(f"Hello, *{user_name}*\!\n\nThe *TRON* is already connected\.\n\nPress *TON to add TON*\.", parse_mode="MarkdownV2", reply_markup=kbrd.net)
    else:
        await message.answer(f"Greetings, {user_name}! You here to connect wallets to the account. Choose any of them, to go on.", reply_markup=kbrd.net)
        return
    await message.answer(f"What do you want to do now\?\n\n*Get more tokens or withdraw the USDT on ur wallet*\.", parse_mode="MarkdownV2", reply_markup=kbrd.balance)

@router.callback_query(F.data=='cex')
async def get_tokens(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await callback.message.answer("You've used CEX to add the balance. The support team will contact u in minutes")
    await bot.send_message(chat_id=settings.GROUP_CHAT_ID, text=f"<b>{user_id}, {username}</b> putted money with a CEX.\n\n, contact him to get more info", parse_mode="HTML")

@router.callback_query(F.data=='tokens')
async def get_tokens(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=0)
    await callback.message.answer("Please enter the amount in USDT you want to add to your balance:")
    await state.set_state(WalletStates.amount_usdt)

@router.callback_query(F.data=='usdt')
async def get_tokens(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action=1)
    await callback.message.answer("Please enter the amount in USDT you want to withdraw from your balance:")
    await state.set_state(WalletStates.withdraw_usdt)

@router.message(WalletStates.withdraw_usdt)
async def amount_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        withdraw_usdt = int(message.text)
        await state.update_data(withdraw_usdt=withdraw_usdt)
        
        balance = db.get_balance(user_id)
        balance_usdt = balance[0]
        if balance_usdt >= withdraw_usdt and withdraw_usdt > 49:
            await message.answer(f"You have ${balance_usdt} on ur balance. Choose the currency to withdraw.", reply_markup=kbrd.net_2)
        elif withdraw_usdt < 50:
            await message.answer("You can't withdraw less then $50. Enter another $USDT.")
        else:
            await message.answer("The withdrawing is in progress! You will get your funds in <b>24h.</b>", parse_mode="HTML")
    except ValueError:
        await message.answer("Invalid amount. Please enter a valid number.")

@router.message(WalletStates.amount_usdt)
async def amount_handler(message: Message, state: FSMContext):
    try:
        amount_usdt = int(message.text)
        if amount_usdt <= 0:
            raise ValueError("Amount must be positive.")
        await state.update_data(amount_usdt=amount_usdt, request_time=datetime.now().timestamp())
        await message.answer("Please choose the net for sending to the wallet address:", reply_markup=kbrd.net_2)
    except ValueError:
        await message.answer("Invalid amount. Please enter a valid number.")

@router.callback_query(F.data.in_(['ton_2', 'tron_2']))
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    currency = callback.data
    result = db.check_wallet(user_id)
    data = await state.get_data()
    
    if not data:
        await callback.message.answer("Oops, try again with /start")
        return

    amount_usdt = data.get('amount_usdt')
    withdraw_usdt = data.get('withdraw_usdt')
    action = data.get('action')

    if action == 0:
        if currency == 'tron_2' and result[0]:
            await callback.message.answer(f"Please send `{amount_usdt}` USDT to the wallet address: `{settings.TRON_WALLET}` \nThen press done", reply_markup=kbrd.done, parse_mode="MarkdownV2")
            await state.update_data(currency='tron')
        elif currency == 'ton_2' and result[1]:
            comment = random.randint(1,100000)
            crypto_data = requests.get(settings.TON_USDT_KEY)   
            crypto_data_json = crypto_data.json()
            amount_ton = (amount_usdt / float(crypto_data_json['price']))
            amount_ton = f"{amount_ton:.3f}"
            await state.update_data(comment=comment, amount_ton=amount_ton)
            await callback.message.answer(f"Please send `{str(amount_ton).replace('.', '\\.')}` TON to the wallet address: `{settings.TON_WALLET}`\n And add comment: `{comment}`", reply_markup=kbrd.done, parse_mode="MarkdownV2")
            await state.update_data(currency='ton')
        else:
            await callback.message.answer("You don't have wallet connected to here.")
            return
            
    elif action == 1:
        withdraw_usdt_without_fees = float(withdraw_usdt) * 0.7
        if currency == 'tron_2' and result[1]:
            await state.update_data(currency='tron')
            await callback.message.answer("Please wait! You will get funds in 24h.")
            db.withdraw_balance(user_id, withdraw_usdt)
            await bot.send_message(chat_id=settings.GROUP_CHAT_ID, text=f"New withraw is requested by <b>{user_id}</b>.\n\n USDT wants: <b>{withdraw_usdt}</b>, USDT send: <b>{withdraw_usdt_without_fees}</b>\n\n <b>{result[1]}</b>", parse_mode="HTML")
        elif currency == 'ton_2' and result[0]:
            await state.update_data(currency='ton')
            await callback.message.answer("Please wait! You will get funds in 24h.")
            db.withdraw_balance(user_id, withdraw_usdt)
            await bot.send_message(chat_id=settings.GROUP_CHAT_ID, text=f"New withraw is requested by <b>{user_id}</b>.\n\n USDT wants: <b>{withdraw_usdt}</b>, USDT send: <b>{withdraw_usdt_without_fees}</b>\n\n <b>{result[0]}</b>", parse_mode="HTML")
        else:
            await callback.message.answer("You don't have wallet connected to here.")
            return
        await state.clear()

@router.callback_query(F.data == 'ok')
async def comfirm_sending(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    amount_usdt = data.get('amount_usdt')
    request_time = data.get('request_time', 0)
    comment = data.get('comment')
    ton_amount = data.get('amount_ton')
    currency = data.get('currency')

    if currency == 'tron':
        wallet_data = db.check_wallet(user_id)
        if not wallet_data:
            await callback.message.answer("Wallet not found. Please link a wallet first.")
            return

        wallet_address = wallet_data[1]
        transactions = crypto.get_tron_usdt_transactions(settings.TRON_WALLET, settings.API_TRON_KEY)
        filtered_transactions = [
            tx for tx in transactions if tx['sender'] == wallet_address and abs(float(tx['amount']) - float(amount_usdt)) < 0.0001 and tx['timestamp'] > crypto.format_timestamp(request_time * 1000)
        ]
        
        if filtered_transactions:
            db.update_balance(amount_usdt, user_id)
            new_balance = db.get_balance(user_id)
            await callback.message.reply(f"Transaction confirmed! Your new balance is: {new_balance} USDT")
        else:
            await callback.message.answer("No matching transaction found. Please check your transaction or try again.")
            await asyncio.sleep(2)
            await callback.message.answer("<b>Attention!!! If putted deposit is from the CEX (Binance, OKX, etc.), press that button!</b>", parse_mode="HTML", reply_markup=kbrd.cex)

    elif currency == 'ton':
        wallet = db.check_wallet(user_id)
        user_address = wallet[0]
        transactions = crypto.get_ton_transactions(user_address)
        
        if not transactions:
            await callback.answer("No transactions found for this address.")
            return

        e_wallet = crypto.change_format(settings.TON_WALLET)[:45]
        
        for tx in transactions:
            out_msgs = tx.get('out_msgs', [])
            amount_ton = ton_amount
            
            if out_msgs:
                for msg in out_msgs:
                    message = msg.get('message')
                    destination = msg.get('destination')[:45]
                    sents = float(msg.get('value', 0)) / 1e9

                    if destination == e_wallet and comment == message:
                        formated_amount_ton = float(amount_ton)
                        if sents == formated_amount_ton:
                            crypto_data = requests.get(settings.TON_USDT_KEY)   
                            crypto_data_json = crypto_data.json()
                            usdt = (formated_amount_ton * float(crypto_data_json['price']))

                            await callback.message.answer(f"<b>Transaction confirmed</b> You've sent {amount_ton} TON. ", parse_mode="HTML")
                            db.update_balance(user_id, usdt)
                            return
                        else:
                            await callback.answer(f"No matching amount of TON is found. Please check if you've sent {amount_usdt} TON.")
                            await callback.answer(f"If you sent another Value of TON, not {amount_usdt} TON. Please text support")
                            await asyncio.sleep(2)
                            await callback.message.answer("<b>Attention!!! If putted deposit is from the CEX (Binance, OKX, etc.), press that button!</b>", parse_mode="HTML", reply_markup=kbrd.cex)

@router.callback_query(F.data.in_(['ton', 'tron']))
async def create_wallet(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    currency = callback.data
    result = db.check_wallet(user_id)

    if (currency == 'ton' and result[0]) or (currency == 'tron' and result[1]):
        await callback.message.answer(f"You already have the {currency.upper()} wallet.")
        return

    await state.set_state(wallet.address)
    await state.update_data(currency=currency)
    await callback.message.answer(f"Send your {currency.upper()} wallet address.")

@router.message(wallet.address)
async def wallet_handler(message: Message, state: FSMContext):
    address = message.text
    random_float = f"{random.uniform(0.001, 0.3):.3f}"
    await state.update_data(random_float=random_float, address=address)
    
    if crypto.is_ton_address(address):
        await message.answer(f"To confirm that this wallet belongs to you, send *exactly* `{random_float}` TON to the address below:\n\nAddress: `{settings.TON_WALLET}`", reply_markup=kbrd.done, parse_mode="MarkdownV2")
    elif crypto.is_trc20_address(address):
        await message.answer(f"To confirm that this wallet belongs to you, send *exactly* `{random_float}` TRX to the address below:\n\nAddress: `{settings.TRON_WALLET}`", reply_markup=kbrd.done, parse_mode="MarkdownV2")
    else:
        await message.answer("It's not TON net address, please double check!")

@router.callback_query(F.data == 'done')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data:
        await callback.message.answer("Oops... press /start")
        return

    user_address = data.get("address")
    currency = data.get('currency')
    expected_amount = float(data.get('random_float'))
    user_id = callback.from_user.id
    request_time = data.get('request_time', 0)

    await state.update_data(amount_usdt=expected_amount, request_time=datetime.now().timestamp())

    if currency == 'ton':
        transactions = crypto.get_ton_transactions(user_address)
        if transactions:
            transactions_found = True
            for tx in transactions:
                out_msgs = tx.get('out_msgs', [])
                for msg in out_msgs:
                    destination = msg.get('destination')
                e_wallet = crypto.change_format(settings.TON_WALLET)
                f_destination = destination[:45]
                f_e_wallet = e_wallet[:45]
                if f_destination == f_e_wallet:
                    for msg in out_msgs:
                        sents = msg.get('value')
                    sents = float(sents) / 1e9
                    if abs(sents - expected_amount) < 1e-6:
                        await callback.message.answer(f"<b>Transaction confirmed</b> You've sent {expected_amount} TON.", parse_mode="HTML")
                        db.create_wallet_ton(user_id, user_address)
                        return
            if not transactions_found:
                await callback.answer("No transactions found for this address.")
            else:
                await callback.answer(f"No matching transaction found. Please check if you've sent {expected_amount} TON.")

    if currency == 'tron':
        transactions = crypto.get_tron_transactions(settings.TRON_WALLET, settings.API_TRON_KEY)
        filtered_transactions = [
            tx for tx in transactions if tx['sender'] == user_address and abs(float(tx['amount']) - float(expected_amount)) < 0.0001 and tx['timestamp'] > crypto.format_timestamp(request_time * 1000)
        ]

        if filtered_transactions:
            db.create_wallet_tron(user_id, user_address)
            await state.clear()
        else:
            await callback.message.answer("No matching transaction found. Please check your transaction or try again.")
    
    db.create_balance(user_id)
