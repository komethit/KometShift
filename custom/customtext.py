import tkinter as tk
from settings import *
import re
import tkinter.font as tkfont


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = "customtext" + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        self.editorFont = tkfont.Font(font=self["font"])
        self.tabSize = self.editorFont.measure(pref.textarea["measure"])
        self.config(tabs=self.tabSize)
        if pref.textarea["autoindent"]:
            self.bind("<Return>", self.autoindent)
        if pref.textarea["autoindentbracket"]:
            self.bind(":", self.autoindentBrakcet)
        if pref.textarea["autoclosebracket"]:
            self.bind("<KeyRelease>", self.autoBracketClose)

    def autoindentBrakcet(self, event):
        line = self.get("insert linestart", "insert lineend")
        match = re.match(r"^(\s+)", line)
        current_indent = len(match.group(0)) if match else 0
        new_indent = current_indent + 4
        self.insert("insert", event.char + "\n" + " " * new_indent)
        return "break"

    def autoBracketClose(self, event):
        matching = pref.textarea["brackets"].get(event.char, None)
        if matching:
            event.widget.insert("insert", matching)
            event.widget.mark_set("insert", "insert-1c")

    def autoindent(self, event):
        line = self.get("insert linestart", "insert")
        match = re.match(r"^(\s+)", line)
        whitespace = match.group(0) if match else ""
        self.insert("insert", f"\n{whitespace}")
        return "break"

    def _proxy(self, *args):
        """checking for movement of the scrollbar of the text field"""
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
            if (
                args[0] in ("insert", "replace", "delete")
                or args[0:3] == ("mark", "set", "insert")
                or args[0:2] == ("xview", "moveto")
                or args[0:2] == ("xview", "scroll")
                or args[0:2] == ("yview", "moveto")
                or args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="tail")
            return result
        except:
            pass
