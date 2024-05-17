from aiogram.filters import Filter
from aiogram.types import Message
from idActions import *
class MessageFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
    def isCorrectFunction(self, userStatus):
        statusFunctions = {
                    "creator": ["/start", "создать уведомление", "добавить админа", "удалить админа", "записаться", "whatsapp", "telegram", "удалить"],
                    "admin": ["/start", "создать уведомление", "whatsapp", "telegram"], "customer": ["/start", "записаться"]}
        return self.my_text.lower() in statusFunctions[userStatus]
    async def __call__(self, message: Message) -> bool:
        self.userStatus = getUserStatus(getUserId(message))
        return (message.text.lower() == self.my_text.lower() and self.isCorrectFunction(self.userStatus))



# class MyFilter(Filter):
#     def __init__(self, my_text, userStatus) -> None:
#         self.my_text = my_text
#         self.userStatus = userStatus
#
#     def isCorrectFunction(my_text: str, userStatus: str):
#         statusFunctions = {
#             "creator": ["/start", "создать уведомление", "добавить админа", "удалить удмина", "записаться"],
#             "admin": ["/start", "создать уведомление"], "customer": ["/start", "записаться"]}
#         return my_text in statusFunctions[userStatus]
#
#     async def __call__(self, message: Message) -> bool:
#         print(self.isCorrectFunction(userStatus=self.userStatus))
#         return (message.text == self.my_text) and (self.isCorrectFunction(userStatus=self.userStatus))