def getIdFromFile(name): #теперь запросы из бд
    filesCollection = {"creators":"creatorsId", "admins":"adminsId"}
    with open(filesCollection[name.lower()]) as file:
        fileId = [str(i).replace("\n", "") for i in file]
    return fileId

def getUserId(message):
    return str(message.from_user.id)

def getUserStatus(userId): #теперь запросы в бд
    if userId in getIdFromFile("creators"):
        return "creator"
    elif userId in getIdFromFile("admins"):
        return "admin"
    else:
        return "customer"

