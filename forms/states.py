from aiogram.fsm.state import StatesGroup, State
class Status(StatesGroup):
    waitingCustomerInfo = State() # Задаем состояние
    waitingMessengerSelection = State()
    waitingAdminInfo = State()