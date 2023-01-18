from tkinter import *
from tkinter import ttk
from settings import *

class RecentFileWidget(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)
        self.heading('#0', text=lang['widgets']['recentfiles'])
        self.bind('<BackSpace>', self.removeItem)
        self.bind("<Motion>", self.highlight_row)
        
    def highlight_row(self, event):
        tree = event.widget
        item = tree.identify_row(event.y)
        tree.tk.call(tree, "tag", "remove", "highlight")
        tree.tk.call(tree, "tag", "add", "highlight", item)
        
    def style(self):
        self.tag_configure('highlight', background=theme['editor']['widgets']['background-hover'])
        ttk.Style(self).configure('Treeview.Heading', font=theme['editor']['text']['font']['font-normal'], foreground=theme['editor']['text']["foreground-gray"])
        self.column('#0', width=140)
        ttk.Style(self).map(
            "Treeview",
            background=[("selected", theme['editor']['widgets']["background-select"])],
            foreground=[("selected", theme['editor']['text']["foreground-select"])],
        )
        ttk.Style(self).configure(
            "Treeview",
            bordercolor="#red",
            indent=prefs['editor']['treeview-widget']["indent"],
            background=theme['editor']['widgets']["subground"],
            font=theme['editor']['text']['font']['font-normal'],
            fieldbackground=theme['editor']['widgets']["subground"],
            foreground=theme['editor']['text']["foreground"],
        )
        
    def removeItem(self, event): 
        try:
            selected_items = self.selection()
            self.delete(selected_items)
        except: pass
        
    def addNewRecent(self, path):
        newpath = path.split('/')[-1]
        self.insert('', 'end', None, text=newpath, tags=[path])
        
    def _onClickedNode(self, function):
        try:
            curItem = self.focus()
            function(self.item(curItem)['tags'][0])
        except: pass