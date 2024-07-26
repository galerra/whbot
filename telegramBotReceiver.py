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
from message import *
import psycopg2
from threading import Thread
import time
from dbFiles.tableNotifications import Notifications
from dbFiles.tableStaff import Staff
from dbFiles.tableHistory import History
from aiogram import types
from record import Record
from user import User
from whatsappActions import *
from aiogram.types import FSInputFile
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
# adminsNames = {"815109033":"Артем", "5193475349":"Виктор", "878095267":"Сергей"} #из бд


@dp.message(Command('активировать'))
async def requestPassword(message: types.Message, state: FSMContext):
    keyboard = await getBackwardKeyboard()
    await message.answer(":", reply_markup= keyboard)
    await state.set_state(Status.waitingCommandPassword)

@dp.message(Status.waitingCommandPassword)
async def activateTables(message: types.Message, state: FSMContext):
    password = message.text
    if password == config.commandPassword:

        db = History()
        if not(db.isExist()):
            db.createTable()
            await message.answer("Была создана таблица History")

        db = Notifications()
        if not(db.isExist()):
            db.createTable()
            await message.answer("Была создана таблица Notifications")

        db = Staff()
        if not(db.isExist()):
            db.createTable()
            db.insertToTable(("Шуруха", "Артем", "Викторович", "creator", "815109033", "89614951406"))
            await message.answer("Была создана таблица Staff")
        await message.answer("Все таблицы были активированы")
    else:
        await state.clear()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    company = config.companyName
    userId = getUserId(message)
    user = User(userId)
    keyboard = user.getStarterKeyboard()
    await message.answer(f"Привет, я бот-менеджер компании <b>{company}</b>!", reply_markup=keyboard, parse_mode="html")

@dp.message(Command('Назад'))
async def backward(message: types.Message, state: FSMContext):
    await state.clear()
    userId = getUserId(message)
    user = User(userId)
    await message.reply(text="Перехожу назад...", reply_markup=user.getStarterKeyboard())


@dp.message(MessageFilter('Удалить'))
async def setNotification(message: types.Message):
    db = Notifications()
    db.deleteTable()
    await message.reply("Удалено!")

isFree = True
def queryDetection(allRecords : list):
    records = allRecords
    global isFree
    isFree = False
    for record in records:
        message = InstantlyMessage()
        hour = int(getTimeDict(record.time)["hour"])
        if hour < 22:
            message.editText(record.getData())
            sendMessageToUser(record.numberPhone, message.getText())  # отправка первоначального уведомления
        else:
            print("Больше 22")
    isFree = True


def checkNotifications():
    idDeletedRecords = []
    while True:
        db = Notifications()
        for deletedId in idDeletedRecords:
            db.deleteRecordById(str(deletedId))
        idDeletedRecords = []
        records = db.selectData()
        if (records is not None) and isFree:
            for db_record in records:
                record = Record(db_record)
                currentDate = dateNormalized(getCurrentDate())
                if currentDate == record.date:
                    remainingTime = record.timeToRecord()
                    if remainingTime <= 3600: #до записи осталось не менее часа
                        idDeletedRecords.append(record.id)
                        if remainingTime >= 1800: #запись не менее чем через полчаса
                            message = NotificationMessage()
                            message.editText(record.getData())
                            sendMessageToUser(record.numberPhone, message.getText())
                        db_history = History()
                        db_history.insertToTable((record.numberPhone, record.date, record.time, record.adminId, record.masterName))
                elif currentDate > record.date: #если после включения текущая текущая дата оказалась больше той, что в записи
                    idDeletedRecords.append(record.id)
                    db_history = History()
                    db_history.insertToTable((record.numberPhone, record.date, record.time, record.adminId, record.masterName))


checkNotificationsThread = Thread(target=checkNotifications, daemon=True)
checkNotificationsThread.start()




@dp.message(MessageFilter('Создать запись'))
async def setNotification(message: types.Message, state: FSMContext):
    await state.set_state(Status.waitingRecordInfo)
    keyboard = await getBackwardKeyboard()
    await message.reply("89614951406 10.02.24 12:00 - пример, как нужно писать", reply_markup=keyboard)


@dp.message(Status.waitingRecordInfo)
async def getCustomerInfo(message: types.Message, state: FSMContext):
    allRecords = [record for record in message.text.split("\n")]
    correctRecords = []
    textErrors = ""
    textCorrects = ""
    for i in range(len(allRecords)):
        record = allRecords[i].split()
        record.insert(3, getUserId(message))
        record = Record(record)
        allTests = [record.checkPhone(), record.checkDate(), record.checkTime()]
        isCorrect = True
        for test in allTests:
            if test != "OK":
                isCorrect = False
                textErrors += f"В записи под номером {i + 1} есть ошибка: \n - {test}.\nЯ обработаю остальные записи, а эту вы можете исправить и отправить мне заново. \n\n"
        if isCorrect:
            correctRecords.append(record)
            textCorrects += f"Запись {i + 1}/{len(allRecords)}:\n " \
                            f"Телефон: {record.numberPhone}\n" \
                            f"Дата: {record.date}\n" \
                            f"Время: {record.time}\n" \
                            f"Мастер: {record.masterName}\n\n"
    if len(correctRecords) != 0: #т.е. есть хотя бы одна правильно оформленная запись
        await state.update_data(info=correctRecords)
        await state.set_state(Status.waitingMessengerSelection)
        keyboard = createMessengerSelectionKeyboard()
        await message.answer(text=textCorrects, reply_markup=keyboard.as_markup())
        if len(textErrors) != 0: await message.answer(text=textErrors)
    else:
        await message.answer(text=textErrors)
        await state.clear()


@dp.callback_query(F.data == "WhatsApp")
async def tapToWhatsApp(callback: types.CallbackQuery, state:FSMContext):
    records = await state.get_data()
    records = records["info"]
    if len(records) != 0:
        firstDetectionThread = Thread(target=lambda: queryDetection(records))
        firstDetectionThread.start()

        dataBase = Notifications()
        for record in records:
            dataBase.insertToTable((record.numberPhone, record.date, record.time, record.adminId, record.masterName))
        await state.clear()
        await callback.message.answer("Записано!")

    else:
        await callback.message.answer("Кнопка уже была нажата после последнего добавления данных")

@dp.message(MessageFilter('Расписание'))
async def setNotification(message: types.Message):
    userId = getUserId(message)
    db = Notifications()
    data = db.selectData()
    recordsDict = {}
    for record in data:
        record = Record(record)
        if userId == record.adminId:
            recordsDict[record.getIntDateTime()] = record
    recordsDict = {key: recordsDict[key] for key in sorted([x for x in recordsDict.keys()])}

    text = ""
    c = 0
    for record in recordsDict.values():
        c += 1
        text += f"{c}. {record.date} {record.time}\n"
    if len(text) == 0:
        await message.reply("Нет записей, созданных вами/для вас")
    else:
        await message.reply(text)


@dp.message(MessageFilter('Добавить сотрудника'))
async def getAddingWorkerInfo(message: types.Message, state: FSMContext):

    await message.reply("Введи следующие параметры:\n"
                        "ФИО\n"
                        "Статус\n"
                        "Telegram id\n"
                        "Телефон")
    await state.set_state(Status.waitingAdminInfo)

@dp.message(Status.waitingAdminInfo)
async def addWorker(message: types.Message, state: FSMContext):
    text = message.text
    text = tuple(text.split())
    db = Staff()
    db.insertToTable(text)
    await state.clear()


@dp.message(MessageFilter('Удалить сотрудника'))
async def getDeletionUserInfo(message: types.Message, state: FSMContext):
    await message.reply("Введи Telegram id пользователя:")
    await state.set_state(Status.waitingDeletionWorker)


@dp.message(Status.waitingDeletionWorker)
async def deleteWorker(message: types.Message, state: FSMContext):
    telegramId = message.text
    db = Staff()
    db.deleteRecordByTelegramId(telegramId)
    await message.reply("Удалено!")
    await state.clear()


@dp.message(Command('+сотрудник'))
async def getNewWorkerInfo(message: types.Message, state: FSMContext):
    await message.reply("Чтобы попасть в команду, необходимо иметь один из этих статусов:\n"
                        "- master\n"
                        "- admin\n"
                        "Заполни информацию, и мы рассмотрим заявку.")
    await message.reply("Введи следующие параметры:\n"
                        "- ФИО\n"
                        "- Желаемый статус\n"
                        "- Телефон")
    await state.set_state(Status.waitingUserInfo)


@dp.message(Status.waitingUserInfo)
async def sendNewWorkerInfo(message: types.Message, state: FSMContext):
    await message.reply("Отлично! Если ты действительно сотрудник, то скоро тебе выдадут доступ")
    info = message.text.split()
    telegramId = getUserId(message)
    info = {"userSurname": info[0], "userName": info[1], "userPatronymic": info[2], "desiredStatus": info[3], "numberPhone": info[4], "telegramId": telegramId, "currentStatus": getUserStatus(telegramId)}
    message = NewWorkerMessage()
    message.editText(info)

    global isFree
    isFree = False
    db = Staff()
    creatorPhone = (db.getPhoneByStatus("creator"))[0] #функция возвращает tuple, но creator единственный, поэтому можно обратиться к первому элементу
    sendMessageToUser(creatorPhone, message.getText())
    isFree = True

    await state.clear()

@dp.message(MessageFilter('Войти'))
async def signIn(message: types.Message):
    await message.answer("Через 30 секунд я пришлю сюда по очереди 3 QR-кода. Сканируйте их в том же порядке, в котором они идут, пока не войдете в систему.")
    await message.answer("Я присылаю скриншоты несколько раз, так как QR-код может измениться, пока вы его сканируете.")


    global isFree
    isFree = False

    holdingWhatsappThread = Thread(target=lambda: holdingWhatsapp(20))
    holdingWhatsappThread.start()

    for i in range(3):
        time.sleep(20)
        screen = FSInputFile("wh.png")
        await message.answer_photo(screen)
        await message.answer("QR-код может скоро измениться, поторопитесь!")

    await message.answer("Если вы не смогли войти, то запустите функцию еще раз!")
    await message.answer("Если вы не знаете, вошли ли вы, то также запустите функцию и посмотрите на скриншот.")
    isFree = True


@dp.message(MessageFilter('Удалить запись'))
async def getRecordsForUser(message: types.Message, state: FSMContext):
    db = Notifications()
    allRecords = db.selectData()
    userId = getUserId(message)
    text = ""
    for record in allRecords:
        record = Record(record)
        if userId == record.adminId:
            data = record.getData()
            text += f"{data['id']}: {data['numberPhone']} {data['date']} {data['time']} {data['masterName']}\n"
    keyboard = await getBackwardKeyboard()
    if len(text) != 0:
        await message.answer("Введите цифру(номер) записи, которую хотите удалить", reply_markup=keyboard)
        await message.answer(text)
    else:
        await message.answer("Нет записей, созданных вами/для вас", reply_markup=keyboard)
    await state.set_state(Status.waitingIdDeletableRecord)

@dp.message(Status.waitingIdDeletableRecord)
async def deleteRecordByUser(message: types.Message):
    recordId = message.text
    if not(recordId.isdigit()):
        await message.answer("Проверьте, что ввели число")
    else:
        user = User(getUserId(message))
        userId = user.telegramId
        db = Notifications()
        adminId = db.getAdminIdById(recordId)
        if userId == adminId:
            db.deleteRecordById(recordId)
            await message.answer("Запись удалена из базы данных")
        else:
            await message.answer("Вы ввели не свой номер записи")


@dp.message(MessageFilter('Все записи'))
async def selectionRecordsPeriod(message: types.Message):
    db = Notifications()
    records = db.selectData() #массив с tuple`ами
    records = [Record(record) for record in records]

    text = getTextSortingRecords(records)
    keyboard = await getBackwardKeyboard()
    await message.answer("Вот текущие записи у каждого сотрудника:\n\n" + text, reply_markup=keyboard)
    keyboard = await createPeriodSelectionKeyboard()
    await message.answer("Если вы хотите посмотреть все прошедшие записи, то выберите период:", reply_markup=keyboard.as_markup())

@dp.callback_query(F.data == "Week")
async def getWeekRecords(callback: types.CallbackQuery):
    currentWeekday = getCurrentWeekday()
    currentDay = getCurrentDay()

    if currentDay < 8:
        startDay = 1
    else:
        startDay = currentDay - currentWeekday

    stopDay = currentDay
    allDates = [date for date in range(startDay, stopDay + 1)]

    db = History()
    records = db.selectData()
    records = [Record(record) for record in records]

    suitableRecords = []
    for record in records:
        date = getDateDict(record.date)
        if int(date["year"]) == getCurrentYear() and int(date["month"]) == getCurrentMonth() and int(date["day"]) in allDates:
            suitableRecords.append(record)

    text = getTextSortingRecords(suitableRecords)
    await callback.message.answer("Вот прошедшие записи за текущую неделю (каждого первого числа сброс):\n\n" + text)

@dp.callback_query(F.data == "Month")
async def getMonthRecords(callback: types.CallbackQuery):
    db = History()
    records = db.selectData()
    records = [Record(record) for record in records]
    records = [record for record in records if int((getDateDict(record.date))["month"]) == getCurrentMonth()]
    text = getTextSortingRecords(records)
    await callback.message.answer("Вот прошедшие записи за текущий месяц:\n\n" + text)

@dp.callback_query(F.data == "Year")
async def getMonthRecords(callback: types.CallbackQuery):
    db = History()
    records = db.selectData()
    records = [Record(record) for record in records]
    records = [record for record in records if int((getDateDict(record.date))["year"]) == getCurrentYear()]
    text = getTextSortingRecords(records)
    await callback.message.answer("Вот прошедшие записи за текущий год:\n\n" + text)



@dp.message(F.text)
async def with_puree(message: types.Message):
    await message.reply("Некорректная функция")



async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

