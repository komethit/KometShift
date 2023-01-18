from tkinter import *
import tkinter as tk
from custom.widgets.text import *
from custom.widgets.linenumbers import *
from settings import theme, prefs
from custom.widgets.terminal import TerminalWidget
from custom.widgets.minimap import MinimapWidget
from utils.utils import FilesUtil
from custom.widgets.toolbar import ToolBar
from syntax.highlight import SyntaxHighlightUtil
from custom.widgets.treeview import TreeManeger
from custom.widgets.recentfiles import RecentFileWidget
from custom.widgets.headers import HeaderWidget
from utils.package import Packages
from custom.tools.wikipediaS import SearchWidget
from custom.widgets.markdown import MarkDownEditorWidget
from menubar import MenuBar

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.editorTextarea = TextWidget(self, undo=True, autocomplete=self.getmatches)
        if theme['editor']['config']['custom-styles']:
            self.editorTextarea.style()
            
        self.md = MarkDownEditorWidget(self)
        self.md.pack_forget()
            
        self.editorMinimap = MinimapWidget(self.editorTextarea)
        if theme['editor']['config']['custom-styles']:
            self.editorMinimap.style()
            
        self.editorRecentFiles = RecentFileWidget(self)
        if theme['editor']['config']['custom-styles']:
            self.editorRecentFiles.style()
            
        self.editorTreeview = TreeManeger(self)
        if theme['editor']['config']['custom-styles']:
            self.editorTreeview.style()

        self.editorToolsFrame = ToolBar(self, background=theme['editor']['widgets']["background"])
        if theme['editor']['config']['custom-styles']:
            self.editorToolsFrame.style()
        self.editorToolsFrame._updateToolBar(self.editorTextarea)
        
        self.editorLinenumbers = TextLineNumbersWidget(self, width=theme['editor']['widgets-config']['linebar']['width'])
        if theme['editor']['config']['custom-styles']:
            self.editorLinenumbers.style()
        self.editorLinenumbers.attach(self.editorTextarea)

        
        self.editorTerminal = TerminalWidget(self)
        if theme['editor']['config']['custom-styles']:
            self.editorTerminal.style()

        # * Adding widgets to the screen
        if prefs['editor']['toolbar']:
            self.editorToolsFrame.pack(side=prefs['editor']['toolbar-widget']['side'], fill=prefs['editor']['toolbar-widget']['fill'], expand=prefs['editor']['toolbar-widget']['expand'])
        if prefs['editor']['terminal']:
            self.editorTerminal.pack(side=prefs['editor']['terminal-widget']['side'], fill=prefs['editor']['terminal-widget']['fill'], expand=prefs['editor']['terminal-widget']['expand'])
        if prefs['editor']['recentfile']:
            self.editorRecentFiles.pack(side=prefs['editor']['recentfile-widget']['side'], fill=prefs['editor']['recentfile-widget']['fill'], expand=prefs['editor']['recentfile-widget']['expand'])
        if prefs['editor']['treeview']:
            self.editorTreeview.pack(side=prefs['editor']['treeview-widget']['side'], fill=prefs['editor']['treeview-widget']['fill'], expand=prefs['editor']['treeview-widget']['expand'])
        if prefs['editor']['linebar']:
            self.editorLinenumbers.pack(side=prefs['editor']['linebar-widget']['side'], fill=prefs['editor']['linebar-widget']['fill'], expand=prefs['editor']['linebar-widget']['expand'])
        if prefs['editor']['textarea']:
            self.editorTextarea.pack(side=prefs['editor']['textarea-widget']['side'], fill=prefs['editor']['textarea-widget']['fill'], expand=prefs['editor']['textarea-widget']['expand'])
        if prefs['editor']['minimap']:
            self.editorMinimap.pack(side=prefs['editor']['minimap-widget']['side'], fill=prefs['editor']['minimap-widget']['fill'], expand=prefs['editor']['minimap-widget']['expand'])
        
        # * File Until Binds widgets
        self.fu = FilesUtil(self, self.editorTextarea, self.editorTerminal, self.editorTreeview)

        # * Highlight syntax system
        SyntaxHighlightUtil(self.editorTextarea).highlight()
        SyntaxHighlightUtil(self.md.editor).highlight()
        
        # * Binds widgets
        self.editorTextarea.bind("<<Change>>", self._OnChanageEditorArea)
        self.editorTextarea.bind("<Configure>", self._OnChanageEditorArea)
        self.editorTreeview.bind("<<TreeviewSelect>>", lambda str: self.editorTreeview._onClickedNode(self.fu.openFilePath))
        self.editorTreeview.bind('<Double-1>', lambda str: self.editorTreeview._addNewRecent(self.editorRecentFiles.addNewRecent))
        self.editorRecentFiles.bind("<<TreeviewSelect>>", lambda str: self.editorRecentFiles._onClickedNode(self.fu.openFilePath))
        
        self.sw = SearchWidget()
        self.menubar = MenuBar(self, self.fu, self.selfopenMarkDown, self.selfopenEditor, self.sw.ask)
        self.menubar.drawMenuBar()
        self.pkg = Packages(self.menubar.packgaes, self.fu)
        self.pkg.insertMenus()
        
    def _OnChanageEditorArea(self, event):
        self.editorLinenumbers.redraw()
        
    def selfopenMarkDown(self):
        try:
            self.md.pack_forget()
        except: pass
        self.editorTextarea.pack_forget()
        self.editorLinenumbers.pack_forget()
        self.md.pack(side=prefs['editor']['textarea-widget']['side'], fill=prefs['editor']['textarea-widget']['fill'], expand=prefs['editor']['textarea-widget']['expand'])
    
    def selfopenEditor(self):
        try:
            self.editorTextarea.pack_forget()
            self.editorLinenumbers.pack_forget()
        except:pass
        self.editorLinenumbers.pack(side=prefs['editor']['linebar-widget']['side'], fill=prefs['editor']['linebar-widget']['fill'], expand=prefs['editor']['linebar-widget']['expand'])
        self.editorTextarea.pack(side=prefs['editor']['textarea-widget']['side'], fill=prefs['editor']['textarea-widget']['fill'], expand=prefs['editor']['textarea-widget']['expand'])
        try:
            self.md.pack_forget()
        except: pass
        
    def getmatches(self, word):
        words = js['MATCHES']
        matches = [x for x in words if x.startswith(word)]
        return matches