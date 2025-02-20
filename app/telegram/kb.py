from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

class Keyboards:
    def __init__(self):
        self.net = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="TON", callback_data=('ton'))],
                           [InlineKeyboardButton(text="TRON", callback_data=('tron'))]])

        self.net_2 = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="TON", callback_data=('ton_2'))],
                           [InlineKeyboardButton(text="TRON", callback_data=('tron_2'))]])

        self.done = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Done", callback_data=('ok'))]])

        self.balance = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Get more tokens", callback_data=('tokens'))],
                           [InlineKeyboardButton(text="Withdraw", callback_data=('usdt'))]])

        self.cex = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="I used CEX", callback_data=('cex'))]])

        self.confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Done", callback_data='done')]])

# Create instance
kbrd = Keyboards()
