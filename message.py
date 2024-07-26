class Message():
    text = ""

    def __init__(self):
        self.text = self.__class__.text

    def getText(self):
        return self.text

    def editText(self, params: dict):
        for key in params.keys():
            self.text = self.text.replace(key, params[key])


class InstantlyMessage(Message):
    text = "Благодарим вас за запись в наш барбершоп!\nВаш мастер: masterName \nДата визита: date\n🕘Время визита: time\n\nСпасибо за доверие к нашему барбершопу! Мы уверены, что вы останетесь довольны нашим сервисом. \nДо встречи в Britva! "


class NotificationMessage(Message):
    text = "Здравствуйте! Рады напомнить, что в time у вас запись в наш барбершоп.\nmasterName также всё помнит и с удовольствием примет Вас. С уважением, команда барбершопа Britva"


class NewWorkerMessage(Message):
    text = "Заявку отправил новый человек!\n" \
           "ФИО: userSurname userName userPatronymic\n" \
           "Номер: numberPhone \n" \
           "Telegram id: telegramId \n\n" \
           "Текущий статус: currentStatus \n" \
           "Желаемый статус: desiredStatus"





