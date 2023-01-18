from tkinter import *
from settings import *

class HeaderWidget(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
         
    def style(self):
        self.configure(
            font=theme['editor']['text']['font']['font-normal'],
            foreground=theme['editor']['text']['foreground'],
            background=theme['editor']['widgets']['background']
        )