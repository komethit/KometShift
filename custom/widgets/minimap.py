from tkinter import *
from settings import *

class MinimapWidget(Text):
    count = 0
    def __init__(self, master, cnf={}, **kw):
        MinimapWidget.count += 1
        parent = master.master
        peerName = "peer-{}".format(MinimapWidget.count)
        if str(parent) == ".":
            peerPath = ".{}".format(peerName)
        else:
            peerPath = "{}.{}".format(parent, peerName)
        master.tk.call(master, 'peer', 'create', peerPath, *self._options(cnf, kw))
        BaseWidget._setup(self, parent, {'name': peerName})
        
    def style(self):
        self.configure(state="disabled", 
                       font=theme['editor']['text']['font']['font-map'], 
                       width=60, 
                       background=theme['editor']['widgets']['background'], 
                       highlightthickness=theme['editor']['config']['border'],
                       wrap=prefs['editor']['textarea-widget']['wrap'])