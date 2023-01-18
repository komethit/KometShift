from tkinter import *
from tkinter import ttk
from settings import prefs, theme, lang
import os
from tkinter import PhotoImage


class TreeManeger(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)
        self.folderImage = PhotoImage(file="./assets/public/folder.png")
        self.specfolderImage = PhotoImage(file="./assets/public/spec-folder.png")
        self.pyfolderImage = PhotoImage(file="./assets/public/py-folder.png")
        self.KometShiftfolderImage = PhotoImage(file="./assets/public/KometShift-folder.png")
        self.pythonImage = PhotoImage(file="./assets/public/python.png")
        self.jsonImage = PhotoImage(file="./assets/public/bracket.png")
        self.fileImage = PhotoImage(file="./assets/public/file.png")
        self.imageImage = PhotoImage(file="./assets/public/image.png")
        self.nodes = {}
        self.currentdirpath = "."
        self.heading('#0', text=lang['widgets']['filemaneger'])
        abspath = os.path.abspath(self.currentdirpath)
        self.dir = abspath
        self._insertNode("", abspath, abspath)
        self.bind("<<TreeviewOpen>>", self._openNode)
        self.bind("<Double-1>", self._addNewRecent)
        self.bind("<Motion>", self.highlight_row)
        
    def highlight_row(self, event):
        tree = event.widget
        item = tree.identify_row(event.y)
        tree.tk.call(tree, "tag", "remove", "highlight")
        tree.tk.call(tree, "tag", "add", "highlight", item)
        
    def style(self):
        self.tag_configure('highlight', background=theme['editor']['widgets']['background-hover'])
        ttk.Style(self).configure('Treeview.Heading', font=theme['editor']['text']['font']['font-normal'], foreground=theme['editor']['text']["foreground-gray"])
        self.column('#0', width=220)
        ttk.Style(self).map(
            "Treeview",
            background=[("selected", theme['editor']['widgets']["background-select"])],
            foreground=[("selected", theme['editor']['text']["foreground-select"])],
        )
        ttk.Style(self).configure(
            "Treeview",
            width=300,
            bordercolor="#red",
            indent=prefs['editor']['treeview-widget']["indent"],
            background=theme['editor']['widgets']["subground"],
            font=theme['editor']['text']['font']['font-normal'],
            fieldbackground=theme['editor']['widgets']["subground"],
            foreground=theme['editor']['text']["foreground"],
        )
        
    def _addNewRecent(self, functions):
        try:
            item = self.selection()[0]
            parent_iid = self.parent(item)
            node = []
            while parent_iid != "":
                node.insert(0, self.item(parent_iid)["text"])
                parent_iid = self.parent(parent_iid)
            i = self.item(item, "text")
            path = os.path.join(*node, i)
            if os.path.isfile(path):
                try:
                    functions(path)
                except TypeError: pass
        except IndexError: pass

    def _reloadNode(self, path):
        self._deleteNodes()
        abspath = os.path.abspath(path)
        self.currentdirpath = abspath
        self._insertNode("", abspath, abspath)

    def _onClickedNode(self, function):
        item = self.selection()[0]
        parent_iid = self.parent(item)
        node = []
        while parent_iid != "":
            node.insert(0, self.item(parent_iid)["text"])
            parent_iid = self.parent(parent_iid)
        i = self.item(item, "text")
        path = os.path.join(*node, i)
        if os.path.isfile(path):
            function(path)

    def _insertNode(self, parent, text, abspath):
        if not text == prefs['editor']['treeview-widget']["remove-tree-word"]:
            if os.path.isdir(abspath):
                if abspath.split('/')[-1] in prefs['editor']['treeview-widget']['spec-folder']:
                    node = self.insert(
                        parent, "end", text=text, open=False, image=self.specfolderImage
                    )
                elif abspath.split('/')[-1] == '__pycache__':
                    node = self.insert(
                        parent, "end", text=text, open=False, image=self.pyfolderImage
                    )
                elif abspath.split('/')[-1] == '.KometShift':
                    node = self.insert(
                        parent, "end", text=text, open=False, image=self.KometShiftfolderImage
                    )
                else:
                    node = self.insert(
                        parent, "end", text=text, open=False, image=self.folderImage
                    )
            elif os.path.splitext(abspath)[-1] == ".py":
                node = self.insert(
                    parent, "end", text=text, open=False, image=self.pythonImage
                )
            elif os.path.splitext(abspath)[-1] == ".json":
                node = self.insert(
                    parent, "end", text=text, open=False, image=self.jsonImage
                )
            elif os.path.splitext(abspath)[-1] == ".png":
                node = self.insert(
                    parent, "end", text=text, open=False, image=self.imageImage
                )
            else:
                node = self.insert(
                    parent, "end", text=text, open=False, image=self.fileImage
                )
            if os.path.isdir(abspath):
                self.nodes[node] = abspath
                self.insert(node, index="end")

    def _openNode(self, event):
        node = self.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.delete(self.get_children(node))
            for p in os.listdir(abspath):
                self._insertNode(node, p, os.path.join(abspath, p))

    def _deleteNodes(self):
        x = self.get_children()
        for item in x:
            self.delete(item)