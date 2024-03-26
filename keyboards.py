from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

def buildCreatorBoard():
    kb = [
        [
            types.KeyboardButton(text="Создать уведомление"),
            types.KeyboardButton(text="Добавить админа"),
            types.KeyboardButton(text="Удалить админа"),
            types.KeyboardButton(text="Записаться")
        ],
           ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard

def buildAdminBoard():
    kb = [
        [
            types.KeyboardButton(text="Создать уведомление"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard

def buildCustomerBoard():
    kb = [
        [
            types.KeyboardButton(text="Записаться"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
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