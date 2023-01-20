import re, json
#with open(f'./syntax/types/python.lang.json', 'r') as f1: js = json.load(f1)
#line = ''
#for i in js:
    #line = line+'{'+f"js['{i.upper()}']['regex']"+"}"+"|"
#line = line[:-1]
#print(line)
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re, json
from settings import prefs, theme

def read(lang):
    global js
    with open(f'./syntax/types/{lang}.lang.json', 'r') as f1: js = json.load(f1)
read(prefs["current-lang"])    

class SyntaxHighlightUtil():
    def __init__(self, root):
        self.root = root
        
    def highlight(self):
        cdg = ic.ColorDelegator()
        cdg.prog = re.compile(rf"{js['keyword']['regex']}|{js['exception']['regex']}|{js['builtin']['regex']}|{js['docstring']['regex']}|{js['string']['regex']}|{js['types']['regex']}|{js['number']['regex']}|{js['classdef']['regex']}|{js['decorator']['regex']}|{js['instance']['regex']}|{js['comment']['regex']}|{js['sync']['regex']}", re.S|re.M)
        cdg.idprog = re.compile(r'(?<!class)\s+(\w+)', re.S)
        cdg.tagdefs = {**cdg.tagdefs, **theme['editor']['syntax']}
        
        self.ipt = ip.Percolator(self.root).insertfilter(cdg)