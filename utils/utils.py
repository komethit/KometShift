from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
import sys
from settings import *


class CreateToolTip(object):
    def __init__(self, widget, text="widget info"):
        self.waittime = prefs['editor']['popup']["waittime"]
        self.wraplength = prefs['editor']['popup']["wraplength"]
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
            font=theme['editor']['text']['font']['font-normal-mini'],
            foreground=theme['editor']['text']['foreground-gray'],
            text=self.text,
            justify="left",
            background=theme['editor']['widgets']['background'],
            relief="solid",
            borderwidth=theme['editor']['config']['border'],
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
        self.currentFilePath = prefs['editor']['file']['deafult']
        self.text.bind("<KeyPress>", self._textOnChanged)

    def about(self):
        win = Toplevel(self.window)
        win.configure(bg=theme['editor']['widgets']['background'])
        lbl1 = Label(
            win,
            font=theme['editor']['text']['font']['font-normal'],
            foreground=theme['editor']['text']['foreground-gray'],
            background=theme['editor']['widgets']['background'],
            text=f"Title - {prefs['editor']['window']['title']}\nVersion - {prefs['editor']['window']['version']}")
        lbl1.pack(padx=20, pady=20)
        win.mainloop()

    def pep8format(self):
        try:
            if (not self.currentFilePath == prefs['editor']['file']["deafult-file-name"] or self.currentFilePath == ""):
                self.terminal.run_command(
                    f'autopep8 --in-place --aggressive --aggressive {self.currentFilePath}')
                self.openFilePath(self.currentFilePath)
            else:
                self.saveSaveAS()
        except BaseException:
            print('Module autopep8 is not installed! "pip install autopep8"')

    def openDirectory(self):
        dir = filedialog.askdirectory()
        self.terminal.run_command(f"cd {dir}")
        self.treeview._reloadNode(dir)

    def openDirectoryPath(self, pth):
        dir = pth
        self.terminal.run_command(f"cd {dir}")
        self.treeview._reloadNode(dir)

    def openFileDialog(self):
        try:
            file = filedialog.askopenfilename()
            self.currentFilePath = file
            self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])
            with open(file, "r") as f:
                self.text.delete(1.0, END)
                self.text.insert(INSERT, f.read())
        except BaseException:
            pass

    def openFilePath(self, path):
        file = path
        self.currentFilePath = file
        self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])
        try:
            with open(file, "r") as f:
                self.text.delete(1.0, END)
                self.text.insert(INSERT, f.read())
        except BaseException:
            pass

    def runFile(self):
        if (not self.currentFilePath == prefs['editor']['file']["deafult"] or self.currentFilePath == ""):
            if run["auto-interpretator"]:
                self.terminal.run_command(
                    f"{sys.executable} {self.currentFilePath}")
            else:
                self.terminal.run_command(
                    f"{run['hand-interpretator']} {self.currentFilePath}"
                )
        else:
            self.saveSaveAS()

    def newFile(self):
        self.currentFilePath = prefs['editor']['file']["deafult"]
        self.text.delete(1.0, END)
        self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])

    def newSavedFile(self):
        try:
            self.text.delete(1.0, END)
            if self.currentFilePath == prefs['editor']['file']["deafult"]:
                self.currentFilePath = filedialog.asksaveasfilename()
            with open(self.currentFilePath, "w") as f:
                f.write(self.text.get("1.0", "end"))
            self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])
        except BaseException:
            pass

    def saveSaveAS(self):
        try:
            if self.currentFilePath == prefs['editor']['file']["deafult"]:
                self.currentFilePath = filedialog.asksaveasfilename()
            with open(self.currentFilePath, "w") as f:
                f.write(self.text.get("1.0", "end"))
            self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])
        except BaseException:
            pass

    def _textOnChanged(self, event):
        self.window.title(prefs['editor']['file']["seporator-ns"]+ prefs['editor']['window']["title"]+ prefs['editor']['file']["seporator-ns"]+' - '+self.currentFilePath.split('/')[-1])

    def _start(self):
        try:
            if len(sys.argv) == 2:
                self.currentFilePath = sys.argv[1]
                self.window.title(prefs['editor']['window']["title"]+' - '+self.currentFilePath.split('/')[-1])
                with open(self.currentFilePath, "r") as f:
                    self.text.delete(1.0, END)
                    self.text.insert(INSERT, f.read())
        except BaseException:
            pass