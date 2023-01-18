import json
import os
from tkinter import filedialog
import tkinter as tk

class Packages:
    def __init__(self, menu, ul):
        self.menu = menu
        self.ul = ul

    def insertMenus(self):
        try:
            for (dirpath, dirnames, filenames) in os.walk("./packages/"):
                for filename in filenames:
                    with open(f"./packages/{filename}", "r") as file:
                        stock = json.load(file)
                        if stock["state"]:
                            if "lang" in stock:
                                with open("./settings/lang/lang.json", "w") as file2:
                                    json.dump(stock["lang"], file2, indent=4)
                            elif "theme" in stock:
                                with open("./settings/themes/theme.json", "w") as file2:
                                    json.dump(stock["theme"], file2, indent=4)
                            elif "run" in stock:
                                with open("./settings/run.json", "w") as file2:
                                    json.dump(stock["run"], file2, indent=4)
                            elif "settings" in stock:
                                with open("./settings/settings.json", "a") as file2:
                                    json.dump(stock["settings"], file2, indent=4)
                            elif "keys" in stock:
                                with open("./settings/keys.json", "w") as file2:
                                    json.dump(stock["keys"], file2, indent=4)
                            else:
                                print(
                                    f'Avalible name of package!; {stock["manifest"]}')
                    if stock['state']:
                        self.menu.add_command(
                            label=stock["manifest"],
                            state=tk.ACTIVE
                        )
                    else:
                        self.menu.add_command(
                            label=stock["manifest"],
                            state=tk.DISABLED
                        )
        except IndexError:
            pass

    def importPackage(self):
        try:
            file = filedialog.askopenfilename()
            with open(file, "r") as fil1:
                stock = json.load(fil1)
                with open(f'./packages/{stock["manifest"]}.json', "w") as fil2:
                    json.dump(stock, fil2, indent=4)
        except BaseException:
            pass