# import random
# instantlyMessage = "Благодарим вас за запись в наш барбершоп!\nВаш мастер: masterName \n🕘Время визита: date time \n\nСпасибо за доверие к нашему барбершопу! Мы уверены, что вы останетесь довольны нашим сервисом. \nДо встречи в Britva! "
# # notificationMessage = "Привет, пишу тебе с напоминанием, что уже скоро твоя запись в барбершоп Britva!\nТебе нужно быть сегодня в time \nmaster тебя будет ждать!"
#
# def notificationMessage():
#     messages = ["Привет, пишу тебе с напоминанием, что уже скоро твоя запись в барбершоп Britva!\nТебе нужно быть сегодня в time \nmaster тебя будет ждать!",
#                 "Уже совсем скоро! Если что, я напоминаю, что запись в наш барбершоп стоит на time\nmaster на месте и будет ждать тебя! Отличного дня!",
#                 "Здравствуйте! Я решил предупредить вас, что сегодня в time у вас запись в наш барбершоп.\nmaster будет во все оружии ждать вас. До скорых встреч!",
#                 "Здравствуйте! Рады напомнить, что в time у вас запись в наш барбершоп.\n master также всё помнит и с удовольствием примет Вас. С уважением, команда барбершопа Britva"
#                 ]
#     return messages[random.randint(0, len(messages) - 1)]


class Message():
    text = ""

    def __init__(self):
        self.text = self.__class__.text

    def getText(self):
        return self.text

    def editText(self, params: dict):
        if "date" in params:
            self.text = self.text.replace("date", params["date"])
        if "time" in params:
            self.text = self.text.replace("time", params["time"])
        if "masterName" in params:
            self.text = self.text.replace("masterName", params["masterName"])


class InstantlyMessage(Message):
    text = "Благодарим вас за запись в наш барбершоп!\nВаш мастер: masterName \n🕘Время визита: date time \n\nСпасибо за доверие к нашему барбершопу! Мы уверены, что вы останетесь довольны нашим сервисом. \nДо встречи в Britva! "


class NotificationMessage(Message):
    text = "Здравствуйте! Рады напомнить, что в time у вас запись в наш барбершоп.\nmasterName также всё помнит и с удовольствием примет Вас. С уважением, команда барбершопа Britva"

