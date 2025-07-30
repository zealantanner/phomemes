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
        self.replFunc = lambda text: replFunc(self.reg,text)
        self.search = lambda text: re.search(self.reg,text)
    # def search(self,text):
    #     return re.search(self.reg,text)
    def sub(self, text:str, count: int = 0, flags = 0) -> str:
        return re.sub(self.reg,self.replFunc(text),text,count,flags)
    def colorsub(self, text:str):
        # return f"{re.split(self.reg, text,1)[0]}{c.color(self.replFunc(text),c.bg.blue)}{re.split(self.reg, text,1)[-1]}"
        array = text.partition(self.reg)
        return f"{array[0]}{colors.color(self.replFunc(text),colors.bg.blue)}{array[2]}"
    
    def to_Patterns(dict:dict):
        array = []
        for thing in dict:
            array.append(
                Pattern(f"{colors.color(thing,colors.bg.red)} to {colors.color(dict[thing],colors.bg.blue)}",
                    thing,
                    lambda *_:dict[thing]
                )
            )
        return tuple(array)
    class Replacing:
        def time(self, reg, text):
            'Replaces valid times'
            search = re.search(reg,text)
            parts = [""]
            parts.append(num2words(search.group(1)))
            if int(search.group(2))<10: parts.append("oh")
            if int(search.group(2))==0: parts.append("clock")
            parts.append(num2words(search.group(2)))
            if search.group(3):
                match re.search(reg,text).group(3).lower():
                    case "am": parts.append("ay em")
                    case "pm": parts.append("pee em")
            parts.append("")
            return " ".join(parts)
        # can I use self.search?
        def currency(self, reg, text, currency="$"):
            pass


periodPauseDelimiters = (".","!","?","\n","\f","\t","\v")
commaPauseDelimiters = (",","~","—","(",")",":",";")
spacePauseDelimiters = (" ","-","_","/","\\")
pauseDelimiters = periodPauseDelimiters + commaPauseDelimiters + spacePauseDelimiters


replacePatterns = (
    Pattern("replace all valid times",
        re.compile(
            r"""
                (?<![\d])      # no extra numbers behind
                ([1-9]|1[0-2]) # 1-12 (1-9 or 10-12)
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
    # Pattern("ordinal numbers, (like 1st 2nd 3rd)",
    #     ,
    #     lambda 
    # ),
    # num2words("1",False,"en","ordinal")
# ---------------------------------------------------------
    Pattern("dashes that should be minus",
        r"-(?=[0-9])+",
        lambda *_:(" minus ")
    ), # can be done with num2words "cardinal"
    # add: detect phone numbers
    Pattern("decimals to point for values",
        r"(?<=[0-9])+\.(?=[0-9])+",
        lambda text,reg:(" point ")
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
    # for prices: (the symbol is pronounced before)
        # make replace function with parameter for the different currencies, like 
        # def currency(reg, text, currency="$")
        # match case for each currency
        # take care of singulars too
    # r"#(?! *\d *)",
    # r"\$(\d+)(\.\d{2})?",
    # "$": " dollar ",
    # "£": " pound ",
    # "€": " euro ",
    # "¥": " yen ",
    # cent is the only one that goes before
    # "¢": " cent ",
    # take care of this by making the cents .54
        # should output 54 cents instead of zero dollars and 54 cents
        # $.54 should also output as 54 cents
    # test to make sure it should be cents for like yen and pounds
)

specialGroupDict = Pattern.to_Patterns({
    " misc.": " miscellaneous ",
    " etc.": " et cetera ",
    ".com": " dot com",
    ".org": " dot org",
    ".net": " dot net",
    ".edu": " dot ee dee you",
    ".gov": " dot guv",
    # can use num2words ordinal for 1st 2nd 3rd etc
    "1st": " first ",
    "2nd": " second ",
    "3rd": " third ",
    "4th": " fourth ",
    "5th": " fifth ",
    "6th": " sixth ",
    "7th": " seventh ",
    "8th": " eighth ",
    "9th": " ninth ",
    "10th": " tenth ",
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