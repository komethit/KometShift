import idlelib.colorizer as ic
import idlelib.percolator as ip
import re, json
from settings import prefs, theme

with open(f'./syntax/types/{prefs["current-lang"]}.lang.json', 'r') as f1: js = json.load(f1)
    
class SyntaxHighlightUtil():
    def __init__(self, root):
        self.root = root
        
    def highlight(self):
        cdg = ic.ColorDelegator()
        cdg.prog = re.compile(rf"{js['KEYWORD']}|{js['BUILTIN']}|{js['EXCEPTION']}|{js['TYPES']}|{js['COMMENT']}|{js['DOCSTRING']}|{js['STRING']}|{js['SYNC']}|{js['INSTANCE']}|{js['DECORATOR']}|{js['NUMBER']}|{js['CLASSDEF']}", re.S|re.M)
        cdg.idprog = re.compile(r'(?<!class)\s+(\w+)', re.S)
        cdg.tagdefs = {**cdg.tagdefs, **theme['editor']['syntax']}
        ip.Percolator(self.root).insertfilter(cdg)
