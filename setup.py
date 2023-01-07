# %%    UTF-8    %%
# %%    author - KometHit, ButterSus    %%
from app import Window  # <---- main python engine script.
from settings import *  # <---- settings json import.
from tools.latest import *  # <---- latest save and write script engine.

# see the modules that you need to download for the application to work.
# run this script to start the program.
# read the github documentation before starting.
if __name__ == "__main__":
    window = Window()
    print('Welcome to KometShift Applications!\nYou can read the documentation in https://github.com/komethit/KometShift')
    window.mainloop()
    if pref.editor["auto-latest-save"]:
        writeLatest(
            {
                "directory": window.editorTreeview.currentdirpath,
                "file": window.fu.currentFilePath,
            }
        )
