from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import sys, json, os, time
from settings import *


class CreateToolTip(object):
    def __init__(self, widget, text="widget info"):
        self.waittime = pref.popup["waittime"]
        self.wraplength = pref.popup["wraplength"]
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            self.tw,
            font=theme.font["font-mini"],
            foreground=theme.foreground["foreground"],
            text=self.text,
            justify="left",
            background=theme.background["subground"],
            relief="solid",
            borderwidth=theme.window["highlightthickness"],
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class FilesUtil:
    def __init__(self, window, textarea, treminal, treeview) -> None:
        self.window = window
        self.text = textarea
        self.treeview = treeview
        self.terminal = treminal
        self.currentFilePath = pref.editor["deafult-file-name"]
        self.text.bind("<KeyPress>", self._textOnChanged)
        
    def pep8format(self):
        try:
            if (
                not self.currentFilePath == pref.editor["deafult-file-name"]
                or self.currentFilePath == ""
            ):
                self.terminal.run_command(f'autopep8 --in-place --aggressive --aggressive {self.currentFilePath}')
                self.openFilePath(self.currentFilePath)
            else:
                self.saveSaveAS()
        except: print('Module autopep8 is not installed! "pip install autopep8"')

    def openDirectory(self):
        dir = filedialog.askdirectory()
        self.terminal.run_command(f"cd {dir}")
        self.treeview._reloadNode(dir)
        print(sys.executable)

    def openDirectoryPath(self, pth):
        dir = pth
        self.terminal.run_command(f"cd {dir}")
        self.treeview._reloadNode(dir)
        print(sys.executable)

    def openFileDialog(self):
        try:
            file = filedialog.askopenfilename()
            self.window.title(pref.window["title"])
            self.currentFilePath = file
            with open(file, "r") as f:
                self.text.delete(1.0, END)
                self.text.insert(INSERT, f.read())
        except:
            pass

    def openFilePath(self, path):
        file = path
        self.window.title(pref.window["title"])
        self.currentFilePath = file
        try:
            with open(file, "r") as f:
                self.text.delete(1.0, END)
                self.text.insert(INSERT, f.read())
        except:
            pass

    def runFile(self):
        if (
            not self.currentFilePath == pref.editor["deafult-file-name"]
            or self.currentFilePath == ""
        ):
            if run["auto-interpretator"]:
                self.terminal.run_command(f"{sys.executable} {self.currentFilePath}")
            else:
                self.terminal.run_command(
                    f"{run['hand-interpretator']} {self.currentFilePath}"
                )
        else:
            self.saveSaveAS()

    def newFile(self):
        self.currentFilePath = pref.editor["deafult-file-name"]
        self.text.delete(1.0, END)
        self.window.title(pref.window["title"])

    def newSavedFile(self):
        try:
            self.text.delete(1.0, END)
            if self.currentFilePath == pref.editor["deafult-file-name"]:
                self.currentFilePath = filedialog.asksaveasfilename()
            with open(self.currentFilePath, "w") as f:
                f.write(self.text.get("1.0", "end"))
            self.window.title(pref.window["title"])
        except:
            pass

    def saveSaveAS(self):
        try:
            if self.currentFilePath == pref.editor["deafult-file-name"]:
                self.currentFilePath = filedialog.asksaveasfilename()
            with open(self.currentFilePath, "w") as f:
                f.write(self.text.get("1.0", "end"))
            self.window.title(pref.window["title"])
        except:
            pass

    def _textOnChanged(self, event):
        self.window.title(
            pref.editor["seporator-ns"]
            + pref.window["title"]
            + pref.editor["seporator-ns"]
        )

    def _start(self):
        try:
            if len(sys.argv) == 2:
                self.currentFilePath = sys.argv[1]
                self.window.title(pref.window["title"])
                with open(self.currentFilePath, "r") as f:
                    self.text.delete(1.0, END)
                    self.text.insert(INSERT, f.read())
        except:
            pass
