import config
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
from sendlers import sendMessageToUser
from datetime import datetime
from conversions import *
from messageExamples import *
import psycopg2
from threading import Thread
import time
from dbFiles.tableNotifications import notifications
from messageExamples import instantlyMessage
from dbFiles.tableHistory import history
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
# adminsNames = {"815109033":"Артем", "5193475349":"Виктор", "878095267":"Сергей"} #из бд


#
#
@dp.message(MessageFilter('Удалить'))
async def setNotification(message: types.Message):
    dataBase = notifications()
    dataBase.deleteData()
    # dataBase.deleteTable()
    # dataBase.createTable()
    await message.reply("Удалено!")
#

firstNotifications = []
def queryDetection(firstNotifications):
    while True:
        removeNotifications = []
        if (len(firstNotifications) != 0):
            for proc in firstNotifications:
                removeNotifications.append(proc)  # это уведомление в очередь на удаление
                message = instantlyMessage.replace("masterName", proc["masterName"]).replace("date", proc["date"]).replace("time", proc["time"])
                sendMessageToUser(proc["number"], message)  # отправка первоначального уведомления
            for ind in range(len(removeNotifications)):
                try:
                    firstNotifications.remove(removeNotifications[ind])
                except:
                    print("В очереди что-то пошло не так!")
                    firstNotifications.clear()
firstDetectionThread = Thread(target=queryDetection, args=(firstNotifications,), daemon=True)
firstDetectionThread.start()

def checkNotifications():
    idDeletedRecords = []
    while True:
        db_notifications = notifications()
        for deletedId in idDeletedRecords:
            db_notifications.deleteRecord((deletedId, ))
        idDeletedRecords = []
        records = db_notifications.selectData()
        if records != None:
            for record in records:
                dateRecord = record[1]
                timeRecord = record[2]
                timeMinusHour = timeRecord
                timeMinusHour = f"{int(timeMinusHour[:2]) - 1}{timeMinusHour[2:]}"
                if recordCompare(dateRecord, timeMinusHour):
                    idRecord = record[0]
                    phone = record[3]
                    adminId = record[4]
                    masterName = record[5]
                    message = notificationMessage().replace("time", timeRecord).replace("master", masterName)
                    sendMessageToUser(phone, message)
                    idDeletedRecords.append(idRecord)
                    db_history = history()
                    db_history.insertToTable((dateRecord, timeRecord, phone, adminId, masterName))


checkNotificationsThread = Thread(target=checkNotifications, daemon=True)
checkNotificationsThread.start()

#
#
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    company = config.companyName
    userId = getUserId(message)
    userStatus = getUserStatus(userId)
    allKeyboards = {"creator": buildCreatorBoard(), "admin": buildAdminBoard(), "customer": buildCustomerBoard()}
    await message.answer(f"Привет, я бот-менеджер компании <b>{company}</b>!", reply_markup=allKeyboards[userStatus], parse_mode="html")

@dp.message(MessageFilter('Создать уведомление'))
async def setNotification(message: types.Message, state: FSMContext):
    await message.reply("89614951406 10.02.24 12:00 - пример, как нужно писать")
    await state.set_state(Status.waitingCustomerInfo)

@dp.message(Status.waitingCustomerInfo)
async def getCustomerInfo(message: types.Message, state: FSMContext):
    info = customerInfoProcessing(message)
    allTests = [checkPhoneNumber(info["number"]), checkRecord(info["date"], info["time"])]
    isCorrect = True
    for test in allTests:
        if test != "OK":
            isCorrect = False
            await message.reply(test)
    if isCorrect:
        keyboard = createMessengerSelectionKeyboard()
        info['date'] = dateNormalized(info['date'])
        await state.update_data(info= info)
        await message.answer(text=f"Если данные верны, выбери мессенджер для уведомления: \n"
                            f"Телефон: {info['number']} \n"
                            f"Дата: {info['date']} \n"
                            f"Время: {info['time']} \n"
                            f"Мастер: {info['masterName']} \n",
                            reply_markup=keyboard.as_markup())
        await state.set_state(Status.waitingMessengerSelection)


@dp.callback_query(F.data == "WhatsApp")
async def tapToWhatsApp(callback: types.CallbackQuery, state:FSMContext):
    userInfo = await state.get_data()
    userInfo = userInfo["info"]
    if len(userInfo) != 0:
        dataBase = notifications()
        print(userInfo)
        dataBase.insertToTable((userInfo["date"], userInfo["time"], userInfo["number"], userInfo["adminId"], userInfo["masterName"]))
        await state.clear()
        firstNotifications.append(userInfo)
        await callback.message.answer("Записано!")
    else:
        await callback.message.answer("Кнопка уже была нажата после последнего добавления данных")

@dp.message(MessageFilter('Расписание'))
async def setNotification(message: types.Message):
    adminId = getUserId(message)
    db = notifications()
    data = db.selectData()
    text = ""
    c = 0
    for record in data:
        dbAdminId = record[4]
        if adminId == dbAdminId:
            visitDate = record[1]
            visitTime = record[2]
            c += 1
            text += f"{c}. {visitDate} {visitTime}\n"
    await message.reply(text)
    # await state.set_state(Status.waitingCustomerInfo)

@dp.message(MessageFilter('Добавить админа'))
async def addAdmin(message: types.Message, state: FSMContext):
    await message.reply("Введи следующие параметры:\n"
                        "ФИО\n"
                        "Статус\n"
                        "Telegram id\n"
                        "Телефон")
    await state.set_state(Status.waitingAdminInfo)

@dp.message(Status.waitingAdminInfo)
async def getAdminInfo(message: types.Message, state: FSMContext):
    text = message.text
    text = tuple(text.split())
    db = staff()
    db.insertToTable(text)
    await state.clear()
#
# @dp.callback_query(F.data == "WhatsApp")
# async def tapToWhatsApp(callback: types.CallbackQuery, state:FSMContext):
#     await callback.answer()
#     userInformation = await state.get_data()
#     callbackMessage = writingNotificationToFile([userInformation["info"]["number"], userInformation["info"]["date"], userInformation["info"]["time"], userInformation["info"]["adminId"]])
#     await callback.message.answer(callbackMessage["message"])
#     if callbackMessage["code"] == 0:
#         await sendMessageToUser(userInformation["info"]["number"], instantlyMessage.replace("adminName", adminsNames[userInformation["info"]["adminId"]]).replace("date", userInformation["info"]["date"]).replace("time", userInformation["info"]["time"]))
#         await sendTimeMessageToUser(userInformation["info"]["number"], notificationMessage, userInformation["info"]["date"], userInformation["info"]["time"])
#
#     await state.clear()
#     if callbackMessage["code"] == 1:
#         await state.set_state(Status.waitingCustomerInfo)
# #

@dp.message(F.text)
async def with_puree(message: types.Message):
    await message.reply("Некорректная функция")


async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

#
#
#
#
#
#
# # def writingNotificationToFile(info: list[str]):
# #     try:
# #         with open("notifications", "w") as file:
# #             for i in range(len(info)):
# #                 file.write(info[i])
# #                 file.write("\n")
# #             file.write("\n")
# #     except:
# #         return {"code": 1, "message":"Произошла ошибка записи в базу данных, пришлите информацию заново"}
# #     return {"code" : 0, "message":"Информация помещена в базу данных"}
# #