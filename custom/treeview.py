from tkinter import *
from tkinter import ttk
from settings import *
import os
from tkinter import PhotoImage


class TreeManeger(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        ttk.Treeview.__init__(self, *args, **kwargs)
        self.folderImage = PhotoImage(file="./assets/folder.png")
        self.pythonImage = PhotoImage(file="./assets/python.png")
        self.jsonImage = PhotoImage(file="./assets/bracket.png")
        self.fileImage = PhotoImage(file="./assets/file.png")
        self.imageImage = PhotoImage(file="./assets/image.png")
        self.nodes = {}
        ttk.Style(self).theme_use(theme.window["ttk:style"])
        ttk.Style(self).map(
            "Treeview",
            background=[("selected", theme.background["background-select"])],
            foreground=[("selected", theme.select["foreground-select"])],
        )
        ttk.Style(self).configure(
            "Treeview",
            bordercolor="#red",
            indent=pref.treeview["indent"],
            background=theme.background["subground"],
            font=theme.font["font-normal"],
            fieldbackground=theme.background["subground"],
            foreground=theme.foreground["foreground"],
        )
        self.currentdirpath = "."
        abspath = os.path.abspath(self.currentdirpath)
        self.dir = abspath
        self._insertNode("", abspath, abspath)
        self.bind("<<TreeviewOpen>>", self._openNode)

    def _openPopup(self, fu, event):
        iid = self.identify_row(event.y)
        if iid:
            self.selection_set(iid)
            parent_iid = self.parent(iid)
            node = []
            while parent_iid != "":
                node.insert(0, self.item(parent_iid)["text"])
                parent_iid = self.parent(parent_iid)
            i = self.item(iid, "text")
            path = os.path.join(*node, i)
            self.contextMenu = Menu(self)
            if os.path.isfile(path):
                self.contextMenu.add_command(
                    label=lang["dropdown"]["new"], state=DISABLED
                )
                self.contextMenu.add_command(
                    label=lang["dropdown"]["new-dir"], state=DISABLED
                )
                self.contextMenu.add_separator()
                self.contextMenu.add_command(
                    label=lang["dropdown"]["run"], state=DISABLED
                )
                self.contextMenu.add_separator()
                self.contextMenu.add_command(label=lang["dropdown"]["delete"][0])
                self.contextMenu.add_separator()
                self.contextMenu.add_command(label=lang["dropdown"]["copy-path"])
            else:
                self.contextMenu.add_command(label=lang["dropdown"]["new"])
                self.contextMenu.add_command(label=lang["dropdown"]["new-dir"])
                self.contextMenu.add_separator()
                self.contextMenu.add_command(
                    label=lang["dropdown"]["run"], state=DISABLED
                )
                self.contextMenu.add_separator()
                self.contextMenu.add_command(
                    label=lang["dropdown"]["delete"][1], state=DISABLED
                )
                self.contextMenu.add_separator()
                self.contextMenu.add_command(label=lang["dropdown"]["copy-path"])
            self.contextMenu.post(event.x_root, event.y_root)
        else:
            pass

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
        if not text == pref.treeview["remove-tree-word"]:
            if os.path.isdir(abspath):
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
