from tkinter import *
from settings import *
try:
    from tkterminal import Terminal
except: print('! tkterminal module is not installed, please install the requirements; pip -r requirements.txt')

class TerminalWidget(Terminal):
    def __init__(self, *args, **kwargs):
        Terminal.__init__(self, *args, **kwargs)
        self.tag_configure('error', foreground=theme['editor']['widgets-config']['terminal']['error'])
        self.tag_configure('basename', foreground=theme['editor']['widgets-config']['terminal']['basename'])
        self.tag_configure('output', foreground=theme['editor']['widgets-config']['terminal']['output'])
        self.shell = prefs['editor']['terminal-widget']['shell']; self.linebar = prefs['editor']['terminal-widget']['linebar']
        self.basename = prefs['editor']['terminal-widget']['basename']
        
    def style(self):
        self.configure(pady=theme['editor']['widgets-config']['pad'][1], 
                       selectbackground=theme['editor']['widgets']['background-select'], 
                       selectforeground=theme['editor']['text']['foreground-select'], 
                       insertwidth=theme['editor']['config']['insert']['insert-width'], 
                       insertbackground=theme['editor']['config']['insert']['insert-color'], 
                       background=theme['editor']['widgets']['subground'], 
                       highlightthickness=theme['editor']['config']['border'], 
                       font=theme['editor']['text']['font']['font-normal'], 
                       padx=theme['editor']['widgets-config']['pad'][0],
                       height=14)
        