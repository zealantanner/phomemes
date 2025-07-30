import re
from contextlib import suppress
from num2words import num2words

class colors:
    '''Colors class:
    Reset all colors with colors.reset\n
    Two subclasses: fg = foreground and bg = background.\n
    Use as colors.subclass.colorname.\n
    i.e. colors.fg.red or colors.bg.green\n
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
    def color(text:str, color):
        return f"{color}{text}{colors.reset}"

class Pattern:
    def __init__(self, desc:str, reg:str, replFunc):
        self.desc = desc
        self.reg = reg
        self.replFunc = lambda text: replFunc(reg,text)
    def sub(self, text:str, count: int = 0, flags = 0) -> str:
        return re.sub(self.reg,self.replFunc(text),text,count,flags)
    def colorsub(self, text:str, count: int = 0, flags = 0) -> str:
        # return f"{re.split(self.reg, text,1)[0]}{c.color(self.replFunc(text),c.bg.blue)}{re.split(self.reg, text,1)[-1]}"
        # array = re.split(self.reg,text)
        # return f"{array[0]}{colors.color(self.replFunc(text),colors.bg.blue)}{array[1]}"
        return re.sub(self.reg,colors.color(self.replFunc(text),colors.bg.blue),text,count,flags)    
    def to_Patterns(dict:dict):
        array = []
        for thing in dict:
            value = dict[thing]
            array.append(
                Pattern(f"{thing} to {value}",
                    re.escape(thing),
                    lambda *_, val=value: val
                )
            )
        return array
    class Replacing:
        def time(reg:str, text:str):
            "Replaces valid times"
            search:str = re.search(reg,text)
            parts = [""]
            parts.append(num2words(search.group(1)))
            if int(search.group(2))<10: parts.append("oh")
            if int(search.group(2))==0: parts.append("clock")
            if int(search.group(2))!=0: parts.append(num2words(search.group(2)))
            if search.group(3):
                match search.group(3).lower():
                    case "am": parts.append("ay em")
                    case "pm": parts.append("pee em")
            parts.append("")
            return " ".join(parts)
        # can I use self.search?
        # class number:
        def number_commas(reg:str, text:str):
            "Replaces commas in numbers"
            search = re.search(reg,text)
            change = "".join(re.search(reg,text).group().split(","))
            print(change)
            return change
            # return re.sub(reg,change,text)
        def ordinal_number(reg:str, text:str):
            "Replaces ordinal numbers like 1st 2nd 3rd"
            search:str = re.search(reg,text)
            parts = [""]
            parts.append(num2words(search.group()[:-2],False,"en","ordinal"))
            return " ".join(parts)+" "
        def currency(reg:str, text:str, currencySymbol="$"):
            search:str = re.search(reg,text)
            def find_plural(num:int, type:str, is_decimal:bool=False):
                names = {
                    "$": ["dollars","dollar","cents","cent"],
                    "£": ["pounds", "pound", "pence","penny"],
                    "€": ["euros",  "euro",  "cents","cent"],
                    "¥": ["yen",    "yen",],
                    "¢": ["cents",  "cent",],
                    }
                move = 0
                if(is_decimal):
                    move = 2
                if(int(num)==1):
                    return names[type][move+1]
                else:
                    return names[type][move]
                # return {"plural": names[type][move], "singular": names[type][move+1]}
            parts = ["","","","","",""]
            # ["","two","dollars","thirteen","cents",""]
            # $£€¥¢
            match currencySymbol:
                case "$"|"£"|"€":
                    if(search.group(5)):            # .12 .00 exists
                        if(int(search.group(3))==0):    # 0.12, 0.00, 0.99
                            if(int(search.group(5))==0):    # 0.00
                                parts[1] = num2words(0)
                                parts[2] = find_plural(0, currencySymbol)
                            if(int(search.group(5))>0):     # 0.12, 0.99
                                parts[3] = num2words(int(search.group(5)))
                                parts[4] = find_plural(int(search.group(5)), currencySymbol, True)
                        if(int(search.group(3))>0):     # 1. 32. 1123.
                            parts[1] = num2words(int(search.group(3)))
                            parts[2] = find_plural(int(search.group(3)), currencySymbol)+","
                            if(int(search.group(5))==0):    # 1.00 32.00 1123.00
                                parts[3] = ""
                                parts[4] = ""
                            if(int(search.group(5))>0):     # 1.12, 321.99
                                parts[3] = num2words(int(search.group(5)))
                                parts[4] = find_plural(int(search.group(5)), currencySymbol, True)
                    else:                           # 1, 3, 1234, 0
                        if(int(search.group(3))==0):    # 0
                            parts[1] = num2words(0)
                            parts[2] = find_plural(0, currencySymbol)
                        if(int(search.group(3))>0):     # 1, 3, 1234
                            parts[1] = num2words(int(search.group(3)))
                            parts[2] = find_plural(int(search.group(3)), currencySymbol)
                case "¢"|"¥":
                    parts[1] = num2words(int(search.group(2)))
                    parts[2] = find_plural(int(search.group(2)), currencySymbol)
            return " ".join(parts)

print(num2words("0.01",False,"en","currency"))
print(num2words("1",False,"en","currency"))
print(num2words("23",False,"en","currency"))
print(num2words("0123"))

periodPauseDelimiters = (".","!","?","\n","\f","\t","\v")
commaPauseDelimiters = (",","~","—","(",")",":",";")
spacePauseDelimiters = (" ","-","_","/","\\")
pauseDelimiters = periodPauseDelimiters + commaPauseDelimiters + spacePauseDelimiters


longReplacePatterns = [
    Pattern("replace all valid times",
        re.compile(
            r"""
                (?<![\d])      # no extra numbers behind
                ([1-9]|1[0-2]) # 1-12 (1-9 10-12)
                :
                ([0-5]\d       # 00-59
                    (?!\d))    # but no numbers after
                \ *            # zero or more spaces
                ([ap]m         # am or pm
                    (?![a-z])  # but no letters after
                )?             # selects am/pm if it's there
            """,
            flags=re.I | re.X),
        lambda reg, text: Pattern.Replacing.time(reg, text)
    ),
# ---------------------------------------------------------
    Pattern("remove \",\" from big numbers",
        r"\d{1,3}(,\d{3})+",
        lambda reg, text: "".join(re.search(reg,text).group().split(","))
    ),
# ---------------------------------------------------------
    Pattern("ordinal numbers, (like 1st 2nd 3rd)",
        re.compile(
            r"""
                \d*            # 0-any numbers
                (              # group
                    (?<!1)         # not 11st 12nd 13rd
                    (1st|2nd|3rd)  # 1st 2nd 3rd
                |              # or
                    [04-9]th       # 0th 4th-9th
                |              # or
                    1[1-3]th       # 11th 12th 13th
                )
                (?![a-z])      # no letters after
            """,
            flags=re.I | re.X),
        lambda reg, text: Pattern.Replacing.ordinal_number(reg, text)
    ),
    # num2words("1",False,"en","ordinal")
# ---------------------------------------------------------
    # currency
    Pattern("$ to dollars",
        r"(\$)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda reg, text: Pattern.Replacing.currency(reg, text, "$")
    ),
    Pattern("£ to pounds",
        r"(£)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda reg, text: Pattern.Replacing.currency(reg, text, "£")
    ),
    Pattern("€ to euros",
        r"(€)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda reg, text: Pattern.Replacing.currency(reg, text, "€")
    ), 
    Pattern("¥ to yen",
        r"(¥)(\d+)",
        lambda reg, text: Pattern.Replacing.currency(reg, text, "¥")
    ),
    Pattern("¢ to cents",
        r"(¢)(\d+)",
        lambda reg, text: Pattern.Replacing.currency(reg, text, "¢")
    ),
# ---------------------------------------------------------
    # add: detect phone numbers
    Pattern("dashes that should be minus",
        r"-(?=[0-9])+",
        lambda *_:(" minus ")
    ), # can be done with num2words "cardinal"
    Pattern("decimals to point for values",
        r"(?<=[0-9])+\.(?=[0-9])+",
        lambda *_:(" point ")
    ), # can be done with num2words "cardinal"
    # dont forget multiple points 12.43.5
    # ([0-9]+)(\.[0-9]+)+
    # numbers with decimals, 12.34
# ---------------------------------------------------------
    # "#" can be hashtag or number
    Pattern("# to hashtag",
        r"#(?! *\d *)",
        lambda *_:(" hashtag ")
    ),
    Pattern("# to number",
        r"#(?= *\d)",
        lambda *_:(" number ")
    ),
# ---------------------------------------------------------
    # abbreviations
    Pattern("ADHD", r"(?<!a-zA-Z\d)(ADHD)(?![a-zA-Z\d])", lambda*_:" ay dee h dee "),
    Pattern("AFAIK", r"(?<!a-zA-Z\d)(AFAIK)(?![a-zA-Z\d])", lambda*_:" as far as I know "),
    Pattern("AITA", r"(?<!a-zA-Z\d)(AITAH?)(?![a-zA-Z\d])", lambda*_:" am I the asshole "),
    Pattern("AMA", r"(?<!a-zA-Z\d)(AMA)(?![a-zA-Z\d])", lambda*_:" ask me anything "),
    Pattern("ELI5", r"(?<!a-zA-Z\d)(ELI5)(?![a-zA-Z\d])", lambda*_:" explain like I'm 5 "),
    Pattern("IIRC", r"(?<!a-zA-Z\d)(IIRC)(?![a-zA-Z\d])", lambda*_:" if I remember correctly "),
    Pattern("IMO", r"(?<!a-zA-Z\d)(IMO)(?![a-zA-Z\d])", lambda*_:" in my opinion "),
    Pattern("IMHO", r"(?<!a-zA-Z\d)(IMHO)(?![a-zA-Z\d])", lambda*_:" in my honest opinion "),
    Pattern("IRL", r"(?<!a-zA-Z\d)(IRL)(?![a-zA-Z\d])", lambda*_:" in real life "),
    Pattern("IRL", r"(?<!a-zA-Z\d)(IRL)(?![a-zA-Z\d])", lambda*_:" in real life "),
    Pattern("NSFL", r"(?<!a-zA-Z\d)(NSFL)(?![a-zA-Z\d])", lambda*_:" not safe for life "),
    Pattern("NSFW", r"(?<!a-zA-Z\d)(NSFW)(?![a-zA-Z\d])", lambda*_:" not safe for work "),
    Pattern("TIFU", r"(?<!a-zA-Z\d)(TIFU)(?![a-zA-Z\d])", lambda*_:" today I fucked up "),
    Pattern("TIL", r"(?<!a-zA-Z\d)(TIL)(?![a-zA-Z\d])", lambda*_:" today I learned "),
    Pattern("TL;DR", r"(?<!a-zA-Z\d)(TL;?DR)(?![a-zA-Z\d])", lambda*_:" too long; didn't read "),
    Pattern("WIP", r"(?<!a-zA-Z\d)(WIP)(?![a-zA-Z\d])", lambda*_:" work in progress "),
    Pattern("YSK", r"(?<!a-zA-Z\d)(YSK)(?![a-zA-Z\d])", lambda*_:" you should know "),

]


specialGroupDict = Pattern.to_Patterns({
    # for abbrevations instead of just space and teh beginning, look for:
        # space, start of string, 
    " misc.": " miscellaneous.",
    " etc.": " et cetera.",
    
    ".com": " dot com",
    ".org": " dot org",
    ".net": " dot net",
    ".edu": " dot ee dee you",
    ".gov": " dot guv",
    # can use num2words ordinal for 1st 2nd 3rd etc
    # "1st": " first ",
    # "2nd": " second ",
    # "3rd": " third ",
    # "4th": " fourth ",
    # "5th": " fifth ",
    # "6th": " sixth ",
    # "7th": " seventh ",
    # "8th": " eighth ",
    # "9th": " ninth ",
    # "10th": " tenth ",
    # make degrees into a function that checks for °[FCK]
    "°F": " degrees fahrenheit ",
    "°C": " degrees celsius ",
    "°K": " degrees kelvin ",
    "°": " degrees ",
})


unknownDict = Pattern.to_Patterns({
    "@": " at ",
    "%": " percent ",
    "&": " and ",
    "*": " asterisk ",

    ">": " is greater than ",
    "<": " is less than ",
    "≥": " is greater than or equal to ",
    "≤": " is less than or equal to ",
    "=": " equals ",
    "≠": " does not equal ",
    "+": " plus ",
    "±": " plus or minus ",
    "∞": " infinity ",
    "π": " pi ",

    "…": ".",
    "⁺": "+",
    "₊": "+",
    "⁻": "-",
    "₋": "-",
    "⁼": "=",
    "₌": "=",
    "⁽": "(",
    "₍": "(",
    "⁾": ")",
    "₎": ")",

    "º": "0",
    "⁰": "0",
    "₀": "0",
    "¹": "1",
    "₁": "1",
    "²": "2",
    "₂": "2",
    "³": "3",
    "₃": "3",
    "⁴": "4",
    "₄": "4",
    "⁵": "5",
    "₅": "5",
    "⁶": "6",
    "₆": "6",
    "⁷": "7",
    "₇": "7",
    "⁸": "8",
    "₈": "8",
    "⁹": "9",
    "₉": "9",
    "⏨": "10",
    
    

    "ₐ": "a",
    "ª": "a",
    "À": "a",
    "à": "a",
    "Á": "a",
    "á": "a",
    "Â": "a",
    "â": "a",
    "Ã": "a",
    "ã": "a",
    "Ä": "a",
    "ä": "a",
    "Å": "a",
    "å": "a",

    "Æ": "ae",
    "æ": "ae",

    "Ç": "c",
    "ç": "c",

    "ₑ": "e",
    "È": "e",
    "è": "e",
    "É": "e",
    "é": "e",
    "Ê": "e",
    "ê": "e",
    "Ë": "e",
    "ë": "e",

    "ƒ": "f",

    "ₕ": "h",
    "ⁱ": "i",
    "Ì": "i",
    "ì": "i",
    "Í": "i",
    "í": "i",
    "Î": "i",
    "î": "i",
    "Ï": "i",
    "ï": "i",

    "ₖ": "k",

    "ₗ": "l",

    "ₘ": "m",

    "ₙ": "n",
    "ⁿ": "n",

    "Ñ": "ny",
    "ñ": "ny",

    "ₒ": "o",
    "Ò": "o",
    "ò": "o",
    "Ó": "o",
    "ó": "o",
    "Ô": "o",
    "ô": "o",
    "Õ": "o",
    "õ": "o",
    "Ö": "o",
    "ö": "o",

    "Œ": "oe",
    "œ": "oe",

    "Ø": "oo",
    "ø": "oo",

    "ₚ": "p",

    "ₛ": "s",
    "Š": "s",
    "š": "s",

    "ß": "ss",
    "ẞ": "ss",

    "ₜ": "t",

    "Ð": "th",
    "ð": "th",
    "Þ": "th",
    "þ": "th",

    "Ù": "u",
    "ù": "u",
    "Ú": "u",
    "ú": "u",
    "Û": "u",
    "û": "u",
    "Ü": "u",
    "ü": "u",

    "ₓ": "x",

    "Ý": "y",
    "ý": "y",
    "Ÿ": "y",
    "ÿ": "y",

    "Ž": "z",
    "ž": "z",



    "½": " 1 half ",
    "⅓": " 1 third ",
    "¼": " 1 fourth ",
    "⅕": " 1 fifth ",
    "⅙": " 1 sixth ",
    "⅐": " 1 seventh ",
    "⅛": " 1 eighth ",
    "⅑": " 1 ninth ",
    "⅒": " 1 tenth ",
    "⅔": " 2 thirds ",
    "⅖": " 2 fifths ",
    "¾": " 3 fourths ",
    "⅗": " 3 fifths ",
    "⅜": " 3 eighths ",
    "⅘": " 4 fifths ",
    "⅚": " 5 sixths ",
    "⅝": " 5 eighths ",
    "⅞": " 7 eighths ",
    
    "↑": " up ",
    "↓": " down ",
    "←": " left ",
    "→": " right ",
})


replacePatterns = unknownDict + specialGroupDict + longReplacePatterns