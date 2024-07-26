from dbFiles.tableStaff import Staff
from aiogram import types


class User():
    def __init__(self, telegramId):
        self.telegramId = telegramId
        db = Staff()
        info = db.getPersonInfo(self.telegramId)
        if info == "NULL":
            self.status = "customer"
        else:
            for key, value in info.items():
                setattr(self, key, value) #получаю все атрибуты пользователя из бд
        self.__setAvailableFunctions__() #задаю атрибут доступных функций, исходя из статуса

    def getData(self):
        return vars(self)

    def __setAvailableFunctions__(self):
        if self.status == "customer":
            self.availableFunctions = ["Записаться", ]
        elif self.status == "worker":
            self.availableFunctions = ["Создать запись", "Расписание", "Удалить запись"]
        elif self.status == "admin":
            self.availableFunctions = ["Создать запись", "Расписание", "Все записи", "Войти", "Удалить запись"]
        elif self.status == "creator":
            self.availableFunctions = ["Создать запись", "Расписание", "Все записи", "Войти", "Удалить", "Стоп", "Удалить сотрудника", "Добавить сотрудника", "Удалить запись"]

    def getAvailableFunctions(self):
        return self.availableFunctions

    def getStarterKeyboard(self):
        availableFunctions = self.getAvailableFunctions()
        if len(availableFunctions) <= 4:
            kb = [[], ]
            for function in availableFunctions:
                kb[0].append(types.KeyboardButton(text=function)) #если не больше 4 функций, то все в один ряд
        else:
            kb = [availableFunctions[i:i + 3] for i in range(0, len(availableFunctions), 3)]
            kb = [[types.KeyboardButton(text=kb[i][j]) for j in range(len(kb[i]))] for i in range(len(kb))] #иначе - по 3 кнопки в ряд

        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        return keyboard

# user = User("815109033")
# print(user.getData())
# print(user.getAvailableFunctions())

