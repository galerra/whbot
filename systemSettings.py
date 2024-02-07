from platform import system
from tkinter import *

def getScreenSize():
    win = Tk()
    return {"width": win.winfo_screenwidth(), "height":win.winfo_screenheight()}
