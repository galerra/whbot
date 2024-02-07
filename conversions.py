import fnmatch
from urllib.parse import quote #quote нужна для преобразования текста в ссылку
def checkPhoneNumber(phoneNumber : str):
    alphabet = "+0123456789-() " # пробел и "-" нужны для тех, кто пишет 8 999 99 99 или 8-999-99-99
    phoneNumber.replace(" ", "")
    for symbol in phoneNumber:
        if not(symbol in alphabet):
            return "Проверьте корректность символов в номере!"
    if not(fnmatch.fnmatch(phoneNumber, "+7*") or fnmatch.fnmatch(phoneNumber, "8*")):
        return "Номер начинается не '+7' или '8'"
    return "OK"

def phoneNormalized(phoneNumber : str):
    phoneNumber.replace("-","").replace("(", "").replace(")", "").replace(" ", "")
    return phoneNumber

def linkProcessing(phoneNumber, message):
    return "https://web.whatsapp.com/send?phone=" + phoneNumber + "&text=" + quote(message)