from aiogram.filters import Filter
from aiogram.types import Message
from idActions import *
from user import User


class MessageFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text.lower()

    async def __call__(self, message: Message) -> bool:
        userId = getUserId(message)
        user = User(userId)
        return message.text.lower() == self.my_text and self.my_text in [function.lower() for function in user.getAvailableFunctions()]



