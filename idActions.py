from dbFiles.tableStaff import staff
import asyncio
# from dbFiles import tableMasters
# from dbFiles import tableOffices
# def getIdFromFile(name): #теперь запросы из бд
#     filesCollection = {"creators":"creatorsId", "admins":"adminsId"}
#     with open(filesCollection[name.lower()]) as file:
#         fileId = [str(i).replace("\n", "") for i in file]
#     return fileId

def getUserId(message):
    return str(message.from_user.id)

def getUserStatus(userId): #теперь запросы в бд
    userId = (userId,)
    db = staff()
    status = db.getStatus(userId)
    if len(status) == 0:
        status = [('creator',)]
    return status[0][0]