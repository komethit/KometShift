from settings import prefs
from app import App
from utils.client.versioncheck import checkversionyes
from tkinter import messagebox

def main():
    window = App()
    window.geometry(prefs['editor']['window']['geometry'])
    window.title(prefs['editor']['window']['title'])
    window.resizable(prefs['editor']['window']['resizable'], prefs['editor']['window']['resizable'])
    window.minsize(prefs['editor']['window']['minimizable'][0], prefs['editor']['window']['minimizable'][1])
    window.mainloop()

if __name__ == "__main__":
    if checkversionyes():main()
    else:
        if messagebox.askquestion('Version', 'New version, do you want to download?') == 'yes': pass
        else:main()