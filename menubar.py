from tkinter import Menu, DISABLED
from settings import lang, keys
import tkinter as tk
import os

class MenuBar():
    def __init__(self, win, fu, f1, f2, f3) -> None:
        self.win = win
        self.fu = fu
        self.f2 = f2
        self.f1 = f1
        self.f3 = f3

    def drawMenuBar(self):
        self.fu._start()
        self.menuApplication = Menu(self.win)

        self.fileDropdown = Menu(self.menuApplication, tearoff=False)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new"],
            command=lambda: self.fu.newFile(),
            accelerator=keys["key.new-file"][0],
        )
        self.win.bind(keys["key.new-file"][1], lambda string: self.fu.newFile())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["new-saved"],
            command=lambda: self.fu.newSavedFile(),
            accelerator=keys["key.new-saved-file"][0],
        )
        self.win.bind(
            keys["key.new-saved-file"][1],
            lambda string: self.fu.newSavedFile)
        self.fileDropdown.add_command(
            label=lang["dropdown"]["open"],
            command=lambda: self.fu.openFileDialog(),
            accelerator=keys["key.open-file"][0],
        )
        self.win.bind(keys["key.open-file"][1],
                lambda string: self.fu.openFileDialog())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["opendir"],
            command=lambda: self.fu.openDirectory(),
            accelerator=keys["key.open-dir"][0],
        )
        self.win.bind(keys["key.open-dir"][1], lambda: self.fu.openDirectory())
        self.fileDropdown.add_separator()
        self.fileDropdown.add_command(
            label=lang["dropdown"]["save"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-file"][0],
        )
        self.win.bind(
            keys["key.save-file"][1],
            lambda string: self.fu.saveSaveAS())
        self.fileDropdown.add_command(
            label=lang["dropdown"]["saveas"],
            command=lambda: self.fu.saveSaveAS(),
            accelerator=keys["key.save-as-file"][0],
        )
        self.win.bind(
            keys["key.save-as-file"][1],
            lambda string: self.fu.saveSaveAS())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["file-drop"], menu=self.fileDropdown
        )
        
        self.editMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.editMenu.add_command(
            label=lang["dropdown"]["undo"],
            command=lambda: self.editorTextarea.edit_undo(),
            accelerator=keys["key.undo"][0],
        )
        self.win.bind(
            keys["key.undo"][1],
            lambda string: self.editorTextarea.edit_undo())
        self.editMenu.add_command(
            label=lang["dropdown"]["redo"],
            command=lambda: self.editorTextarea.edit_redo(),
            accelerator=keys["key.redo"][0],
        )
        self.win.bind(
            keys["key.redo"][1],
            lambda string: self.editorTextarea.edit_redo())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["edit-drop"], menu=self.editMenu
        )
        
        self.builtMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.builtMenu.add_command(
            label=lang["dropdown"]["mark"],
            command=lambda: self.f1(),
            accelerator=keys["key.mark"][0],
        )
        self.win.bind(
            keys["key.mark"][1],
            lambda string: self.f1(),
        )
        self.builtMenu.add_command(
            label=lang["dropdown"]["editor"],
            command=lambda: self.f2(),
            accelerator=keys["key.editor"][0],
        )
        self.win.bind(
            keys["key.editor"][1],
            lambda string: self.f2(),
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["built"], menu=self.builtMenu
        )

        self.prefMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.prefMenu.add_command(
            label=lang["dropdown"]["settings"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
            accelerator=keys["key.settings"][0],
        )
        self.win.bind(
            keys["key.settings"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/settings.json")
            ),
        )
        self.prefMenu.add_separator()
        self.prefMenu.add_command(
            label=lang["dropdown"]["theme"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/themes/theme.json")
            ),
            accelerator=keys["key.theme"][0],
        )
        self.win.bind(
            keys["key.theme"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/themes/theme.json")
            ),
        )
        self.prefMenu.add_command(
            label=lang["dropdown"]["hotkeys"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/keys.json")
            ),
            accelerator=keys["key.hotkeys"][0],
        )
        self.win.bind(
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
        self.win.bind(
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
        self.win.bind(keys["key.run-module"][1], lambda string: self.fu.runFile())
        self.shellMenu.add_command(
            label=lang["dropdown"]["configurerun"],
            command=lambda: self.fu.openFilePath(
                os.path.abspath("./settings/run.json")
            ),
            accelerator=keys["key.run-debug"][0],
        )
        self.win.bind(
            keys["key.run-debug"][1],
            lambda string: self.fu.openFilePath(
                os.path.abspath("./settings/run.json")
            ),
        )
        self.shellMenu.add_separator()
        self.shellMenu.add_command(
            label=lang["dropdown"]["clear"],
            command=lambda: self.editorTerminal.run_command("clear"),
            accelerator=keys["key.run-clear"][0],
        )
        self.win.bind(
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
        self.win.bind(keys["key.virtual"][1], lambda string: None)
        self.shellMenu.add_command(
            label=lang["dropdown"]["pep"],
            command=lambda: self.fu.pep8format(),
            state=DISABLED,
            accelerator=keys["key.pep"][0],
        )
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["shell-drop"], menu=self.shellMenu
        )

        self.helpMenu = tk.Menu(self.menuApplication, tearoff=0)
        self.helpMenu.add_command(
            label=lang["dropdown"]["about"],
            command=lambda: self.fu.about()
        )
        self.helpMenu.add_command(
            label=lang["dropdown"]["wiki"],
            command=lambda: self.f3(),
            accelerator=keys["key.wiki"][0]
        )
        self.win.bind(keys["key.wiki"][1], lambda string: self.f3())
        self.menuApplication.add_cascade(
            label=lang["dropdown"]["help"], menu=self.helpMenu)

        self.win.config(menu=self.menuApplication)