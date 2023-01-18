from tkinter import Text
from settings import prefs, theme
import re
import tkinter.font as tkfont
from syntax.highlight import js

class TextWidget(Text):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None)
        Text.__init__(self, *args, **kwargs)

        self._orig = 'customtext' + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        if prefs['editor']['textarea-widget']['indent-return']:
            self.bind("<Return>", self.autoindent)
        if prefs['editor']['textarea-widget']['indent-bracket']:
            self.bind(":", self.autoindentbracket)
            
        self.font = tkfont.Font(font=self['font'])
        self.tab = self.font.measure('    ') 
        self.config(tabs=self.tab)
        
        self.bind("<Any-KeyRelease>", self._autocomplete)
        self.bind("<Tab>", self._handletab)
        
        self.matches = dict(prefs['editor']['textarea-widget']['matches'])
        
        self.bind("<Motion>", self.hover)
        #self.tag_bind("keyword", "<1>", keyword_click)
        
    def hover(self, event):
        text = event.widget
        keyword_start = text.index(f"@{event.x},{event.y} wordstart")
        keyword_end = text.index(f"@{event.x},{event.y} wordend")
        word = text.get(keyword_start, keyword_end)

        text.tag_remove("keyword", "1.0", "end")

        if word in js['MATCHES']:
            text.mark_set("keyword_start", keyword_start)
            text.mark_set("keyword_end", keyword_end)
            text.tag_add("keyword", keyword_start, keyword_end)

    def _handletab(self, event):
        tag_ranges= self.tag_ranges("autocomplete")
        if tag_ranges:
            self.mark_set("insert", tag_ranges[1])
            self.tag_remove("sel", "1.0", "end")
            self.tag_remove("autocomplete", "1.0", "end")
            return "break"

    def _autocomplete(self, event):
        self.autoclosebracket(event)
        if event.char and self.callback:
            word = self.get("insert-1c wordstart", "insert-1c wordend")
            matches = self.callback(word)
            if matches:
                remainder = matches[0][len(word):]
                insert = self.index("insert")
                self.insert(insert, remainder, ("sel", "autocomplete"))
                self.mark_set("insert", insert)
        
    def autoclosebracket(self, event):
        matching = self.matches.get(event.char, None)
        if matching:
            self.insert("insert", matching)
            self.mark_set("insert", "insert-1c")
        
    def autoindentbracket(self, event):
        line = self.get("insert linestart", "insert lineend")
        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0
        new_indent = current_indent + 4
        self.insert("insert", event.char + "\n" + " "*new_indent)
        return "break"
        
    def autoindent(self, event):
        line = self.get("insert linestart", "insert")
        match = re.match(r'^(\s+)', line)
        whitespace = match.group(0) if match else ""
        self.insert("insert", f"\n{whitespace}")
        return "break"
        
    def style(self):
        self.tag_configure("keyword", background=theme['editor']['widgets']['subground'])
        self.configure(background=theme['editor']['widgets']['background'], 
                       selectbackground=theme['editor']['widgets']['background-select'], 
                       selectforeground=theme['editor']['text']['foreground-select'], 
                       insertwidth=theme['editor']['config']['insert']['insert-width'], 
                       insertbackground=theme['editor']['config']['insert']['insert-color'], 
                       foreground=theme['editor']['text']['foreground'], 
                       highlightthickness=theme['editor']['config']['border'], 
                       font=theme['editor']['text']['font']['font-editor'],
                       pady=theme['editor']['widgets-config']['pad'][1], 
                       padx=theme['editor']['widgets-config']['pad'][0],
                       wrap=prefs['editor']['textarea-widget']['wrap'])

    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
            if (args[0] in ("insert", "replace", "delete") or 
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="tail")
            return result        
        except: pass
