from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio


async def getBackwardKeyboard():
    kb = [[types.KeyboardButton(text="/Назад")],]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard


def createMessengerSelectionKeyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="WhatsApp",
        callback_data="WhatsApp")
    )
    builder.add(types.InlineKeyboardButton(
        text="Telegram",
        callback_data="Telegram")
    )
    return builder

async def createPeriodSelectionKeyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="за неделю",
        callback_data="Week")
    )
    builder.add(types.InlineKeyboardButton(
        text="за месяц",
        callback_data="Month")
    )
    builder.add(types.InlineKeyboardButton(
        text="за год",
        callback_data="Year")
    )
    return builder