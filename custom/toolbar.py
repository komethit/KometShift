from tkinter import *
from settings import *
from tools.utils import *


class ToolBar(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.labelToolRight = Label(
            self,
            foreground=theme.foreground["foreground-gray"],
            text="None",
            background=theme.background["background"],
            font=theme.font["font-mini"],
        )
        self.labelToolRight.pack(side=RIGHT, padx=(0, 10), pady=(0, 4))

        self.labelToolLeft = Label(
            self,
            foreground=theme.foreground["foreground-gray"],
            text="None",
            background=theme.background["background"],
            font=theme.font["font-mini"],
        )
        self.labelToolLeft.pack(side=LEFT, padx=(10, 0), pady=(0, 4))
        if pref.popup["popups"]:
            lbl1 = CreateToolTip(self.labelToolRight, lang["popups"]["label-right"])
            lbl2 = CreateToolTip(self.labelToolLeft, lang["popups"]["label-left"])

    def _updateToolBar(self, editor):
        (line, char) = editor.index(INSERT).split(".")
        totalLine = int(editor.index(END).split(".")[0]) - 1
        self.labelToolRight.configure(
            text=f'{lang["tools"]["line"]} {line}, {lang["tools"]["col"]} {char} - {totalLine} {lang["tools"]["lines"]}    {lang["tools"]["space"]}: {pref.textarea["measureCO"]}    {pref.window["version"]}'
        )
        self.labelToolLeft.configure(
            text=f'{lang["tools"]["wrap"]} {pref.textarea["wrap-mode"]}   {lang["tools"]["title"]} {pref.window["title"]}'
        )
        self.after(100, lambda: self._updateToolBar(editor))
