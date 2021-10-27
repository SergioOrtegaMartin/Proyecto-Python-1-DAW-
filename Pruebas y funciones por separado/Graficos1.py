from tkinter import *
from tkinter import colorchooser



def color():
    root=Tk()
    root.title('Selector de color')
    root.geometry('200x5')
    color=colorchooser.askcolor()
    
    return color

hola=color()

