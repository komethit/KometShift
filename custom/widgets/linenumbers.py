from tkinter import *
from settings import *

class TextLineNumbersWidget(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget
        
    def style(self):
        self.configure(highlightthickness=theme['editor']['config']['border'], background=theme['editor']['widgets']['background'])
        
    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(20, y, fill=theme['editor']['text']['foreground-gray'], font=theme['editor']['text']['font']['font-editor'], anchor="n", text=linenum)
            i = self.textwidget.index("%s+1line" % i)