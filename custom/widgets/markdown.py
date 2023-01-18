from tkinter import Frame, Text, NORMAL, END, DISABLED
import re
from settings import prefs, theme

class MarkDownEditorWidget(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.regexp = re.compile(r"((?P<delimiter>\*{1,3})[^*]+?(?P=delimiter)|(?P<delimiter2>\_{1,3})[^_]+?(?P=delimiter2))")
        self.tags = {1: "italic", 2: "bold", 3: "bold-italic"}
        self.option_add('*Font', theme['editor']['text']['font']['font-editor'])
        
        self.editorfontName = theme['editor']['widgets-config']['markdown']['editorfontName']
        self.displayFontName = theme['editor']['widgets-config']['markdown']['displayFontName']
        
        self.normalSize = theme['editor']['widgets-config']['markdown']['normalSize']
        self.h1Size = theme['editor']['widgets-config']['markdown']['h1Size']
        self.h2Size = theme['editor']['widgets-config']['markdown']['h2Size']
        self.h3Size = theme['editor']['widgets-config']['markdown']['h3Size']

        self.h1Color = theme['editor']['widgets-config']['markdown']['h1Color']
        self.h2Color = theme['editor']['widgets-config']['markdown']['h2Color']
        self.h3Color = theme['editor']['widgets-config']['markdown']['h3Color']
        
        self.editor = Text(
                       self,
                       width=30,
                       background=theme['editor']['widgets']['background'], 
                       selectbackground=theme['editor']['widgets']['background-select'], 
                       selectforeground=theme['editor']['text']['foreground-select'], 
                       insertwidth=theme['editor']['config']['insert']['insert-width'], 
                       foreground=theme['editor']['text']['foreground'], 
                       highlightthickness=theme['editor']['config']['border'], 
                       pady=theme['editor']['widgets-config']['pad'][1], 
                       padx=theme['editor']['widgets-config']['pad'][0],
                       wrap=prefs['editor']['textarea-widget']['wrap'],
                       insertbackground=theme['editor']['config']['insert']['insert-color']
        )
        self.editor.pack(expand=prefs['editor']['markdown']['editor']['expand'], fill=prefs['editor']['markdown']['editor']['fill'], side=prefs['editor']['markdown']['editor']['side'])
        self.editor.bind('<KeyRelease>', self.changes)

        self.display = Text(
                       self,
                       width=30,
                       background=theme['editor']['widgets']['background'], 
                       selectbackground=theme['editor']['widgets']['background-select'], 
                       selectforeground=theme['editor']['text']['foreground-select'], 
                       insertwidth=theme['editor']['config']['insert']['insert-width'], 
                       insertbackground=theme['editor']['config']['insert']['insert-color'], 
                       foreground=theme['editor']['text']['foreground'], 
                       highlightthickness=theme['editor']['config']['border'], 
                       pady=theme['editor']['widgets-config']['pad'][1], 
                       padx=theme['editor']['widgets-config']['pad'][0],
                       wrap=prefs['editor']['textarea-widget']['wrap'],
                       font=f"{self.displayFontName} {self.normalSize}",
        )
        self.display.pack(expand=prefs['editor']['markdown']['display']['expand'], fill=prefs['editor']['markdown']['display']['fill'], side=prefs['editor']['markdown']['display']['side'])
        self.display['state'] = DISABLED
        
        self.editor.tag_config("bold", font=f'{self.displayFontName} {self.normalSize} bold')
        self.editor.tag_config("italic", font=f'{self.displayFontName} {self.normalSize} italic')
        self.editor.tag_config("bold-italic", font=f'{self.displayFontName} {self.normalSize} bold italic')
        
        self.replacements = [
            [
                '(#{1}\s)(.*)',
                'Header 1',
                f'{self.displayFontName} {self.h1Size}', 
                self.h1Color,
                0
            ], [
                '(#{2}\s)(.*)',
                'Header 2', 
                f'{self.displayFontName} {self.h2Size}',
                self.h2Color,
                0
            ], [
                '(#{3}\s)(.*)', 
                'Header 3', 
                f'{self.displayFontName} {self.h3Size}', 
                self.h3Color,
                0        
            ], [
                '\**.+?\**', 
                'Bold', 
                f'{self.displayFontName} {self.normalSize} bold', 
                theme['editor']['text']['foreground'],
                2
            ], [
                '\*.+?\*', 
                'Italic', 
                f'{self.displayFontName} {self.normalSize} italic', 
                theme['editor']['text']['foreground'],
                2
            ], [
                "(\\`{1})(.*)(\\`{1})", 
                'CodeMini', 
                f'{self.displayFontName} {self.normalSize} normal', 
                theme['editor']['widgets-config']['markdown']['codeColor'],
                2
            ], [
                "(\\`{3}\\n+)(.*)(\\n+\\`{3})", 
                'CodeMax', 
                f'{self.displayFontName} {self.normalSize} normal', 
                theme['editor']['widgets-config']['markdown']['linkColor'],
                2
            ], [
                '(\[.*\])(\((http)(?:s)?(\:\/\/).*\))', 
                'Link', 
                f'{self.displayFontName} {self.normalSize} underline', 
                theme['editor']['widgets-config']['markdown']['linkColor'],
                2
            ],
        ]
        self.changes()
    
    def check_markdown(self, start_index="insert linestart", end_index="insert lineend"):
        text = self.editor.get(start_index, end_index)
        for tag in self.tags.values():
            self.editor.tag_remove(tag, start_index, end_index)
        for match in self.regexp.finditer(text):
            groupdict = match.groupdict()
            delim = groupdict["delimiter"]
            if delim is None:
                delim = groupdict["delimiter2"]
            start, end = match.span()
            self.editor.tag_add(self.tags[len(delim)], f"{start_index}+{start}c", f"{start_index}+{end}c")
        return

    def changes(self, event=None):
        self.check_markdown()
        self.display['state'] = NORMAL
        self.display.delete(1.0, END)
        text =self. editor.get('1.0', END)
        textRaw = text
        text = ''.join(text.split('#'))
        text = ''.join(text.split('*'))
        text = ''.join(text.split('`'))
        text = ''.join(text.split('**'))
        self.display.insert(1.0, text)
        for pattern, name, fontData, colorData, offset in self.replacements:
            locations = self.search_re(pattern, textRaw, offset)
            for start, end in locations:
                self.display.tag_add(name, start, end)
            self.display.tag_config(name, font=fontData, foreground=colorData)
        self.display['state'] = DISABLED

    def search_re(self, pattern, text, offset):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end() - offset}")
                )
        return matches

    def rgbToHex(self, rgb):
        return "#%02x%02x%02x" % rgb