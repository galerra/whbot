from aiogram.fsm.state import StatesGroup, State
class Status(StatesGroup):
    waitingUserInfo = State() # Задаем состояние
    waitingMessengerSelection = State()
    waitingAdminInfo = State()
    waitingRecordInfo = State()
    waitingDeletionWorker = State()
    waitingIdDeletableRecord = State()
    waitingCommandPassword = State()