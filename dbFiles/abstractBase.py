from abc import ABC, abstractmethod

class abstractBase(ABC):
    @abstractmethod
    def __init__(self, host, user, password, db_name):
        pass

    @abstractmethod
    def createTable(self):
        pass

    @abstractmethod
    def insertToTable(self, data):
        pass

    @abstractmethod
    def __del__(self):
        pass


















