from tkinter import *
from settings import *


class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        """Connect textbox widget to lines"""
        self.textwidget = text_widget

    def redraw(self, *args):
        """Text line count updates while editing"""
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                23,
                y,
                anchor=N,
                text=linenum,
                fill=theme.foreground["foreground-linenumber"],
                font=theme.font["font"],
            )
            i = self.textwidget.index("%s+1line" % i)
