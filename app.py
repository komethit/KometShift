from tkinter import *
from settings import *
from tkinter import ttk

try:
    from tkterminal import Terminal
except ModuleNotFoundError:
    print('Module tkterminal is not installed! "pip install tkterminal"')
from custom.customtext import *
from tools.packages import *
from custom.linenumbers import *
from syntax.syntaxhighlight import *
from custom.toolbar import *
from custom.treeview import *
from tools.utils import *
from tools.latest import *
import json, os, sys


class Window(Tk):
    def __init__(self, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.geometry(pref.window["geometry"])
        self.title(pref.window["title"])
        self.configure(background='#151515')
        self.minsize(pref.window["minsize"][0], pref.window["minsize"][1])
        self.resizable(pref.window["resizable"][0], pref.window["resizable"][1])

        self.editorToolsFrame = ToolBar(self, background=theme.background["background"])
        self.editorToolsFrame.pack(side=BOTTOM, fill=X, expand=False)

        self.editorTerminal = Terminal(
            pady=theme.window["pad"][0],
            font=theme.font["font"],
            foreground=theme.foreground["foreground"],
            padx=theme.window["pad"][1],
            height=10,
            highlightthickness=theme.window["highlightthickness"],
            background=theme.background["subground"],
            insertbackground=theme.select["insert-color"],
            insertwidth=theme.select["insert-width"],
            selectbackground=theme.select["background-select"],
            selectforeground=theme.select["foreground-select"],
        )
        self.editorTerminal.pack(side=BOTTOM, fill=X, expand=False)

        self.editorTreeview = TreeManeger(self, show="tree")
        self.editorTreeview.pack(fill=Y, side=LEFT, expand=False)

        self.editorFrame = Frame(self)
        self.editorFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.editorTextarea = CustomText(
            self.editorFrame,
            wrap=pref.textarea["wrap-mode"],
            font=theme.font["font"],
            pady=theme.window["pad"][0],
            padx=theme.window["pad"][1],
            background=theme.background["background"],
            foreground=theme.foreground["foreground-editor"],
            insertbackground=theme.select["insert-color"],
            insertwidth=theme.select["insert-width"],
            selectbackground=theme.select["background-select"],
            selectforeground=theme.select["foreground-select"],
            highlightthickness=theme.window["highlightthickness"],
        )
        self.editorTextarea.pack(side=RIGHT, fill=BOTH, expand=True)

        self.editorLinesTextarea = TextLineNumbers(
            self.editorFrame,
            width=40,
            highlightthickness=theme.window["highlightthickness"],
            background=theme.background["background"],
        )
        self.editorLinesTextarea.pack(side=RIGHT, fill=Y, expand=False)

        self.editorLinesTextarea.attach(self.editorTextarea)

        self.editorTextarea.bind("<<Change>>", self.redrawLineNumbers)
        self.editorTextarea.bind("<Configure>", self.redrawLineNumbers)

        self.fu = FilesUtil(
            self, self.editorTextarea, self.editorTerminal, self.editorTreeview
        )

        if pref.textarea["highlight"]:
            Highlight(self.editorTextarea).highlight()

        self.bind(
            "<<TreeviewSelect>>",
            lambda str: self.editorTreeview._onClickedNode(
                function=self.fu.openFilePath
            ),
        )
        # self.bind("<Button-2>", lambda event: self.editorTreeview._openPopup(self.fu, event))

        self.editorTerminal.shell = pref.terminal["shell"]
        self.editorTerminal.basename = pref.terminal["basename"]
        self.editorTerminal.linebar = pref.terminal["linebar"]

        self.editorToolsFrame._updateToolBar(self.editorTextarea)

        if pref.editor["auto-latest-save"]:
            self.fu.openFilePath(loadLatest()["file"])
            self.fu.openDirectoryPath(loadLatest()["directory"])

        self.drawMenuBar()
        self.pkg = Packages(self.packgaes, self.fu)
        self.pkg.insertMenus()

    def redrawLineNumbers(self, event):
        self.editorLinesTextarea.redraw()

    def drawMenuBar(self):
        self.fu._start()
        self.menuApplication = Menu(self)

        self.fileDropdown = Menu(self.menuApplication, tearoff=False)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new"],
            command=lambda: self.fu.newFile(),
            accelerator=keys["key.new-file"][0],
        )
        self.bind(keys["key.new-file"][1], lambda string: self.fu.newFile())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new-saved"],
            command=lambda: self.fu.newSavedFile(),
            accelerator=keys["key.new-saved-file"][0],
        )
        self.bind(keys["key.new-saved-file"][1], lambda string: self.fu.newSavedFile)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["open"],
            command=lambda: self.fu.openFileDialog(),
            accelerator=keys["key.open-file"][0],
        )
        self.bind(keys["key.open-file"][1], lambda string: self.fu.openFileDialog())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["opendir"],
            command=lambda: self.fu.openDirectory(),
            accelerator=keys["key.open-dir"][0],
        )
        self.bind(keys["key.open-dir"][1], lambda: self.fu.openDirectory())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["save"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-file"][0],
        )
        self.bind(keys["key.save-file"][1], lambda string: self.fu.saveSaveAS())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["saveas"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-as-file"][0],
        )
        self.bind(keys["key.save-as-file"][1], lambda string: self.fu.saveSaveAS())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["file-drop"], menu=self.fileDropdown
        )

        self.prefMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.prefMenu.add_command(
            label=lang["dropdown"]["settings"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
            accelerator=keys["key.settings"][0],
        )
        self.bind(
            keys["key.settings"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
        )
        self.prefMenu.add_separator()
        self.prefMenu.add_command(
            label=lang["dropdown"]["theme"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/theme/theme.json")
            ),
            accelerator=keys["key.theme"][0],
        )
        self.bind(
            keys["key.theme"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/theme/theme.json")
            ),
        )
        self.prefMenu.add_command(
            label=lang["dropdown"]["hotkeys"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/keys.json")
            ),
            accelerator=keys["key.hotkeys"][0],
        )
        self.bind(
            keys["key.hotkeys"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/keys.json")
            ),
        )
        self.prefMenu.add_command(
            label=lang["dropdown"]["lang"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/lang/lang.json")
            ),
            accelerator=keys["key.lang"][0],
        )
        self.bind(
            keys["key.lang"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/lang/lang.json")
            ),
        )
        self.packgaes = Menu(self.prefMenu)
        self.prefMenu.add_separator()
        self.prefMenu.add_cascade(
            label=lang["dropdown"]["packages"], menu=self.packgaes
        )
        self.prefMenu.add_separator()
        self.prefMenu.add_cascade(
            label=lang["dropdown"]["packages-import"],
            command=lambda: self.pkg.importPackage(),
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["preferences"], menu=self.prefMenu
        )

        self.shellMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.shellMenu.add_command(
            label=lang["dropdown"]["run"],
            command=lambda: self.fu.runFile(),
            accelerator=keys["key.run-module"][0],
        )
        self.bind(keys["key.run-module"][1], lambda string: self.fu.runFile())
        self.shellMenu.add_command(
            label=lang["dropdown"]["configurerun"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/debug/run.json")
            ),
            accelerator=keys["key.run-debug"][0],
        )
        self.bind(
            keys["key.run-debug"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/debug/run.json")
            ),
        )
        self.shellMenu.add_separator()
        self.shellMenu.add_command(
            label=lang["dropdown"]["clear"],
            command=lambda: self.editorTerminal.run_command("clear"),
            accelerator=keys["key.run-clear"][0],
        )
        self.bind(
            keys["key.run-clear"][1],
            lambda string: self.editorTerminal.run_command("clear"),
        )
        self.shellMenu.add_separator()
        self.shellMenu.add_command(
            label=lang["dropdown"]["virtual"],
            command=lambda: None,
            state=DISABLED,
            accelerator=keys["key.virtual"][0],
        )
        self.bind(keys["key.virtual"][1], lambda string: None)
        self.shellMenu.add_command(
            label=lang["dropdown"]["pep"],
            command=lambda: self.fu.pep8format(),
            accelerator=keys["key.pep"][0],
        )
        self.bind(keys["key.pep"][1], lambda string: None)
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["shell-drop"], menu=self.shellMenu
        )

        self.config(menu=self.menuApplication)
