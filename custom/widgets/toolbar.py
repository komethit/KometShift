from tkinter import *
from settings import *
from utils.utils import *

class ToolBar(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.labelToolRight = Label(self)
        self.labelToolRight.pack(side=RIGHT, padx=(0, 10), pady=(0, 4))

        self.labelToolLeft = Label(self)
        self.labelToolLeft.pack(side=LEFT, padx=(10, 0), pady=(0, 4))
        if prefs['editor']['window']["popups"]:
            lbl1 = CreateToolTip(self.labelToolRight, lang["popups"]["label-right"])
            lbl2 = CreateToolTip(self.labelToolLeft, lang["popups"]["label-left"])
            
    def style(self):
        self.labelToolRight.configure(
            foreground=theme['editor']['text']["foreground-gray"],
            text="None",
            background=theme['editor']['widgets']["background"],
            font=theme['editor']['text']['font']["font-normal-mini"]
        )
        self.labelToolLeft.configure(
            foreground=theme['editor']['text']["foreground-gray"],
            text="None",
            background=theme['editor']['widgets']["background"],
            font=theme['editor']['text']['font']["font-normal-mini"]
        )

    def _updateToolBar(self, editor):
        try:
            (line, char) = editor.index(INSERT).split(".")
            totalLine = int(editor.index(END).split(".")[0]) - 1
            self.labelToolRight.configure(text=f'{lang["tools"]["line"]} {line}, {lang["tools"]["col"]} {char} - {totalLine} {lang["tools"]["lines"]}    {lang["tools"]["space"]}: {prefs["editor"]["textarea-widget"]["measureCO"]}    {prefs["editor"]["window"]["version"]}')
            self.labelToolLeft.configure(text=f'{lang["tools"]["wrap"]} {prefs["editor"]["textarea-widget"]["wrap"]}   {lang["tools"]["title"]} {prefs["editor"]["window"]["title"]}')
            self.after(100, lambda: self._updateToolBar(editor))
        except: pass
