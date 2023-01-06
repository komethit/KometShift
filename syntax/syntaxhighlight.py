import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
from syntax.syntaxtypes import *
from settings import *


class Highlight:
    def __init__(self, text):
        self.txt = text

    def highlight(self):
        cd = ic.ColorDelegator()
        cd.prog = re.compile(
            rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}",
            re.S | re.M,
        )
        cd.idprog = re.compile(r"(?<!class)\s+(\w+)", re.S)
        cd.tagdefs = {**cd.tagdefs, **theme.syntax}
        ip.Percolator(self.txt).insertfilter(cd)
