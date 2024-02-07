from conversions import checkPhoneNumber, phoneNormalized
from whatsappActions import chromeSetup, openWhatsapp, clickOnSendButtom
import time
from selenium.webdriver.support.ui import WebDriverWait

messagesToUsers = ["Уважаемые посетители!"
            "Рады предложить вам наши профессиональные услуги парикмахерского искусства. "
            "Наша парикмахерская, с многолетним опытом работы в этой сфере, гарантирует вам идеальный стиль, индивидуальный подход и безупречное качество."
            "Наша команда состоит из опытных парикмахеров, которые постоянно следят за последними тенденциями в сфере моды и красоты."]
messagesToAdmins = []
def sendMessageToAdmin(number, message):
    print(1)


def sendMessageToUser(userPhone, message, adminPhone):
    if not(checkPhoneNumber(userPhone) == "OK"):
        sendMessageToAdmin("00000", "Ошибка!")
        return
    userPhone = phoneNormalized(userPhone)
    # url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
    driver = chromeSetup()
    wait = WebDriverWait(driver, 30)
    openWhatsapp(userPhone, message, driver)
    clickOnSendButtom(driver, wait)
    time.sleep(5)

    # openWhatsapp(linkProcessing(userPhone, message))
    # time.sleep(connectionTime)
    # clickOnTextBox()
    # time.sleep(1)
    # pg.press("enter")
    # time.sleep(closeTime)
    # closeWhatsapp()






sendMessageToUser("+79614951406", messagesToUsers[0], 1)





        


