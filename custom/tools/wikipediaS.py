from tkinter import *
from settings import *
import wikipedia
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

class SearchWidget():
    def __init__(self):
        wikipedia.set_lang(lang['lang'])
        
    def ask(self):
        try:
            quest = askstring('Seacrh Wikipedia', lang['dropdown']['input'])
            self.search(quest)
        except: pass
    
    def search(self, text):
        try:
            showinfo('Answer', wikipedia.summary(text))
        except: pass
