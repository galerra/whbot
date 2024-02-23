import asyncio
import types
from aiogram import F
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards import *
from idActions import *
from filter import MessageFilter
from forms.states import Status
from sendlers import sendMessageToUser, sendTimeMessageToUser
from datetime import datetime
from conversions import *
from messageExamples import *
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6757354422:AAERiFJx0ysZsH5U1TrwgA99dDUUigTOAgc")
dp = Dispatcher()
adminsNames = {"815109033":"Артем", "5193475349":"Виктор", "878095267":"Сергей"} #из бд

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    company = "Britva" #брать из бд
    userId = getUserId(message)
    userStatus = getUserStatus(userId)
    allKeyboards = {"creator": buildCreatorBoard(), "admin": buildAdminBoard(), "customer": buildCustomerBoard()}
    await message.answer(f"Привет, я бот-менеджер компании <b>{company}</b>!", reply_markup=allKeyboards[userStatus], parse_mode="html")
    print(message.from_user.id)

@dp.message(MessageFilter('Создать уведомление'))
async def setNotification(message: types.Message, state: FSMContext):
    await message.reply("89614951406 10.02.24 12:00 - пример, как нужно писать")
    await state.set_state(Status.waitingCustomerInfo)
    # await sendMessageToUser("+79614951406", "Уведомляю!", 1) #протестить со вторым телефоном

@dp.message(Status.waitingCustomerInfo)
async def getCustomerInfo(message: types.Message, state: FSMContext):
    info = customerInfoProcessing(message.text)
    allTests = [checkPhoneNumber(info["number"]), checkDate(info["date"]), checkTime(info["time"])]
    isCorrect = True
    for test in allTests:
        if test != "OK":
            isCorrect = False
            await message.reply(test)
    if isCorrect:
        info["adminId"] = str(message.from_user.id)
        keyboard = createMessengerSelectionKeyboard()
        await state.update_data(info= info)
        await message.answer(text=f"Если данные верны, выбери мессенджер для уведомления: \n"
                            f"Телефон: {info['number']} \n"
                            f"Дата: {info['date']} \n"
                            f"Время: {info['time']}",
                             reply_markup=keyboard.as_markup())


        # await state.set_state(Status.waitingMessengerSelection)


@dp.callback_query(F.data == "WhatsApp")
async def tapToWhatsApp(callback: types.CallbackQuery, state:FSMContext):
    await callback.answer()
    userInformation = await state.get_data()
    callbackMessage = writingNotificationToFile([userInformation["info"]["number"], userInformation["info"]["date"], userInformation["info"]["time"], userInformation["info"]["adminId"]])
    await callback.message.answer(callbackMessage["message"])
    if callbackMessage["code"] == 0:
        await sendMessageToUser(userInformation["info"]["number"], instantlyMessage.replace("adminName", adminsNames[userInformation["info"]["adminId"]]).replace("date", userInformation["info"]["date"]).replace("time", userInformation["info"]["time"]))
        await sendTimeMessageToUser(userInformation["info"]["number"], notificationMessage, userInformation["info"]["date"], userInformation["info"]["time"])

    await state.clear()
    if callbackMessage["code"] == 1:
        await state.set_state(Status.waitingCustomerInfo)



def writingNotificationToFile(info: list[str]):
    try:
        with open("notifications", "w") as file:
            for i in range(len(info)):
                file.write(info[i])
                file.write("\n")
            file.write("\n")
    except:
        return {"code": 1, "message":"Произошла ошибка записи в базу данных, пришлите информацию заново"}
    return {"code" : 0, "message":"Информация помещена в базу данных"}



@dp.message(F.text)
async def with_puree(message: types.Message):
    await message.reply("Некорректная функция")


async def main():
    await dp.start_polling(bot)






if __name__ == "__main__":
    asyncio.run(main())