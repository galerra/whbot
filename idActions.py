from dbFiles.tableStaff import Staff
import asyncio

def getUserId(message):
    return str(message.from_user.id)

def getUserStatus(userId): #теперь запросы в бд
    userId = (userId,)
    db = Staff()
    status = db.getStatus(userId)
    if len(status) == 0:
        status = 'creator'
    return status