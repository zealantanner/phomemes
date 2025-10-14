import re
from __future__ import annotations
from Qualities import colors, say_span, span, IPA
import Regs



class Pattern:
    def __init__(self, reg:str, func:function, desc:str="Unnamed pattern", type="sets"):
        self.desc = desc
        self.reg = reg
        self.type = type
        if(type == "sets"):
            self.func = lambda span, m: func(span, m)
        elif(type == "text"):
            self.func = lambda text: func(reg, text)


class Token:
    def __init__(self, span:span, text:str="", type=None):
        self.span = span
        self.text = text
        self.type = type
    def __str__(self):
        return self.text
    def __repr__(self):
        return f"{self.__class__.__name__}({colors.color(self.text,colors.bg.green)},\t({self.span}))"

class Word(Token):
    def __init__(self, span:span, text:str="", type=None, pronounceOverride:IPA=None, ):
        super().__init__(span,text,type)
        # self.asif = text if asif is None else asif
        #> type can be acronym
        self.type = type
        if type == "acronym": pass
        #> pronunciation override 

class Delimiter(Token):
    def __init__(self, span:span, text:str="", type=None):
        #> type can be space, comma
        super().__init__(span,text,type)
    types = {
        "period": ".",
        "comma": ",",
        "space": " ",
        "question": "?",
        "exclamation": "!",
        "ellipses": "...",
        "interrobang": "?!",
        "interruption": "-"
    }

class SetNode:
    def __init__(self, span:span, text:str, asif=None, convertby:str=None, inherit_span:bool=False):
        self.span = span
        self.text = text
        # self.asif = text if asif is None else asif
        self.asif = asif
        self.convertby = convertby
        self.inherit_span = inherit_span
        self.children:list[Token|SetNode] = self._split(convertby)
        print(f"creation: {say_span(span)}, \"{self.text}\"")

    def add_child(self, child:Token|SetNode):
        if isinstance(child,SetNode):
            if self.inherit_span:
                child.span = self.span
                child.inherit_span = self.inherit_span
            self.children.append(child)
        elif isinstance(child,Token):
            self.children.append(child)
        else:
            raise ValueError(f"Couldn't add child with type: {type(child)}")
        return child
    def set_children(self, *children:Token|SetNode):
        for child in children:
            self.add_child(child)
        return children
    
    def _split(self, using=None):
        if(using == None):
            for func in Regs.rules:
                pass #>
        # if(using == None):
        #     for patt, in [
        #         Reg.wordspaceword_patt
        #     ]

    def __str__(self):
        return self.text
    def __repr__(self):
        colors["black"]
        return f"{self.__class__.__name__}({colors.bg.green(self.text)},\t({say_span(self.span)}))"
        # return f"Set({self.span[0]},{self.span[1]}), \"{self.text}\")"
