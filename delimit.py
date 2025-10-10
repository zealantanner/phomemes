from __future__ import annotations
import re

periodDelimiters = (".", "!", "?", "\n", "\f", "\t", "\v")
commaDelimiters = (",", "~", "—", "(", ")", ":", ";")
spaceDelimiters = (" ", "-", "_", "/", "\\", "|")
class Group:
    allGroups:list[Group] = [

    ]
    def __init__(self,mark:tuple[str,str], meaning:str, secondary:list[Group]=None):
        self.mark = mark
        self.meaning = meaning
        self.secondary = secondary
        Group.allGroups.append(self)
    def __repr__(self):
        sec = f", secondary={self.secondary.mark[0]}Hello{self.secondary.mark[1]}" if self.secondary else ""
        return f"({self.mark[0]}Hello{self.mark[1]}{sec})"


# allGroups = [
#> use regex if statements and reusing names to make this simple
adict = {
    "doubleq1": (Group(('"','"'), "quotation")),
    "doubleq2": (Group(("“","”"), "quotation")),
    "singleq1": (Group(("'","'"), "quotation")),
    "singleq2": (Group(("‘","’"), "quotation")),
    1: (Group(("¿","?"), "question")),
    2: (Group(("¡","!"), "exclamation")),
    3: (Group(("(",")"), "parentheses")),
    4: (Group(("{","}"), "curly bracket")), #   «...»   ‹...›,
    5: (Group(("[","]"), "bracket")),
    6: (Group(("`","`"), "code")),
    7: (Group(("```","```"), "code block")),
}
adict[3].secondary
Group.allGroups[3].secondary = Group.allGroups[0]
# ]
# all
print(Group.allGroups)
# groups = 


