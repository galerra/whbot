from dbFiles.tableStaff import Staff


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
            self.availableFunctions = ("Записаться")
        elif self.status == "worker":
            self.availableFunctions = ("Создать запись", "Расписание")
        elif self.status == "admin":
            self.availableFunctions = ("Создать запись", "Расписание", "Все записи", "Войти")
        elif self.status == "creator":
            self.availableFunctions = ("Записаться", "Создать запись", "Расписание", "Все записи", "Войти")

    def getAvailableFunctions(self):
        return self.availableFunctions

    def getKeyboard(self):
        availableFunctions = self.getAvailableFunctions()
        kb = []
        for function in availableFunctions:
            kb.append(types.KeyboardButton(text=function))
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        return keyboard

# user = User("815109033")
# print(user.getData())
# print(user.getAvailableFunctions())

