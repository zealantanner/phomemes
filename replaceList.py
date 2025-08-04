import re
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
        def time(reg:str, text:str): # 1:32 3:00 am 12:63
            "Replaces valid times"
            search = re.search(reg,text)
            parts = []
            parts.append(num2words(search.group(1)))
            if int(search.group(2))<10: parts.append("oh")
            if int(search.group(2))==0: parts.append("clock")
            if int(search.group(2))!=0: parts.append(num2words(search.group(2)))
            if search.group(3):
                match search.group(3).lower():
                    case "am": parts.append("A M")
                    case "pm": parts.append("P M")
            return " " + " ".join(parts) + " "
        # can I use self.search?
        # class number:
        def ordinal_number(reg:str, text:str):
            "Replaces ordinal numbers like 1st 2nd 3rd"
            search = re.search(reg,text)
            parts = []
            parts.append(num2words(search.group()[:-2],False,"en","ordinal"))
            return " " + " ".join(parts) + " "
        def currency(reg:str, text:str, currencySymbol="$"):
            "Replaces currencies"
            search = re.search(reg,text)
            def find_plural(num:int, type:str, isdecimal:bool=False):
                names = {
                    "$": ["dollars","dollar","cents","cent"],
                    "£": ["pounds", "pound", "pence","penny"],
                    "€": ["euros",  "euro",  "cents","cent"],
                    "¥": ["yen",    "yen",],
                    "¢": ["cents",  "cent",],
                    }
                move = 0
                if(isdecimal):
                    move = 2
                if(int(num)==1):
                    return names[type][move+1]
                else:
                    return names[type][move]
                # return {"plural": names[type][move], "singular": names[type][move+1]}
            parts = []
            # ["","two","dollars","thirteen","cents",""]
            # $£€¥¢
            match currencySymbol:
                case "$"|"£"|"€":
                    if(search.group(5)):            # .12 .00 exists
                        if(int(search.group(3))==0):    # 0.12, 0.00, 0.99
                            if(int(search.group(5))==0):    # 0.00
                                parts.append(num2words(0))
                                parts.append(find_plural(0, currencySymbol))
                            if(int(search.group(5))>0):     # 0.12, 0.99
                                parts.append(num2words(int(search.group(5))))
                                parts.append(find_plural(int(search.group(5)), currencySymbol, True))
                        if(int(search.group(3))>0):     # 1. 32. 1123.
                            parts.append(num2words(int(search.group(3))))
                            parts.append(find_plural(int(search.group(3)), currencySymbol)+",")
                            # if(int(search.group(5))==0):    # 1.00 32.00 1123.00
                            if(int(search.group(5))>0):     # 1.12, 321.99
                                parts.append(num2words(int(search.group(5))))
                                parts.append(find_plural(int(search.group(5)), currencySymbol, True))
                    else:                           # 1, 3, 1234, 0
                        if(int(search.group(3))==0):    # 0
                            parts.append(num2words(0))
                            parts.append(find_plural(0, currencySymbol))
                        if(int(search.group(3))>0):     # 1, 3, 1234
                            parts.append(num2words(int(search.group(3))))
                            parts.append(find_plural(int(search.group(3)), currencySymbol))
                case "¢"|"¥":
                    parts.append(num2words(int(search.group(2))))
                    parts.append(find_plural(int(search.group(2)), currencySymbol))
            return " " + " ".join(parts) + " "
        
        def phone_number(reg:str, text:str):
            search = re.search(reg,text)
            parts = []
            for part in re.findall(r"\d+",search.group()):
                parts.append(" ".join(map(num2words,re.findall(r"\d",part))))
            print(parts)
            return " " + ", ".join(parts) + " "
            # search = re.search(reg,text)
            # return " " + " ".join(map(num2words,re.findall(r"\d",search.group()))) + " "
        
        def number(reg:str, text:str):
            search = re.search(reg,text)
            parts = ""
            if(float(search.group())==0): # any number that's zero, 0, 0.00, .00
                parts = num2words(0,False,"en","cardinal")
            else:                         # not = 0
                if(search.group(2)): # (0).231, -(3).1, (3), (0)
                    if(int(search.group(2))!=0): # -(3).1, (3), -(4).32136, (5)
                        parts = num2words(float(search.group()),False,"en","cardinal")
                        # parts[1] = num2words(0)
                    if(int(search.group(2))==0): # -(0).1, (0).3213,
                        parts = "".join(num2words(float(search.group())).split("zero",1))
            return " " + parts + " "

class Replace:
    def __init__(self, text:str, patternList:list):
        self.ogtext = text
        self.patternList = patternList
        self.rep = self.__replace_patterns(text,self.patternList)
    def __str__(self):
        return self.rep
    def __replace_patterns(self, text:str,patternList:list) -> str:
        newtext = text
        for pattern in patternList:
            search = re.search(pattern.reg,newtext)
            if(search):
                print(f"replaced \"{colors.color(search.group(),colors.bg.red)}\" with \"{colors.color(pattern.replFunc(newtext),colors.bg.blue)}\" using \"{pattern.desc}\"")
                print(f"{pattern.colorsub(newtext,1)}")
                newtext = pattern.sub(newtext,1)
                newtext = self.__replace_patterns(newtext, patternList)
        return newtext

# Replace.__replace_patterns


# periodDelimiters = (".","!","?","\n","\f","\t","\v")
# commaDelimiters = (",","~","—","(",")",":",";")
# spaceDelimiters = (" ","-","_","/","\\")
# blankDelimiters = ("|")

# pauseDelimiters = periodDelimiters + commaDelimiters + spaceDelimiters
# use | to symbolize a nothing symbol

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
    Pattern("commas in big numbers",
        r"\d{1,3}(,\d{3})+",
        lambda reg, text: "".join(re.search(reg,text).group().split(","))
    ),
# ---------------------------------------------------------
    Pattern("ordinal numbers (like 1st 2nd 3rd)",
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
    Pattern("phone numbers",
        r"(?<!\d)(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)",
        lambda reg, text: Pattern.Replacing.phone_number(reg,text)
    ),
# ---------------------------------------------------------
    # "#" can be hashtag or number
    Pattern("# to \"hashtag\"",
        r"#(?! *\d *)",
        lambda*_:(" hashtag ")
    ),
    Pattern("# to \"number\"",
        r"#(?= *\d)",
        lambda*_:(" number ")
    ),
# ---------------------------------------------------------
    # numbers, can be negative or have decimal
    Pattern("numbers", # this should go after mp3
        r"-?((\d+)(\.(\d+))?|(\.(\d+)))",
        lambda reg, text: Pattern.Replacing.number(reg,text)
    ),
    # Pattern("dashes that should be minus",
    #     r"-(?=[0-9])+",
    #     lambda*_:(" minus ")
    # ), # can be done with num2words "cardinal"
    # Pattern("decimals to point for values",
    #     r"(?<=[0-9])+\.(?=[0-9])+",
    #     lambda*_:(" point ")
    # ), # can be done with num2words "cardinal"
    # dont forget multiple points 12.43.5
    # ([0-9]+)(\.[0-9]+)+
    # numbers with decimals, 12.34
# ---------------------------------------------------------
    # common characters
    Pattern("@ to at", r"@", lambda*_:" at "),
    Pattern("% to percent", r"%", lambda*_:" percent "),
    Pattern("& to and", r"&", lambda*_:" and "),
    Pattern("* to asterisk", r"\*", lambda*_:" asterisk "),
    Pattern("+ to plus", r"\+", lambda*_:" plus "),
    Pattern("> to is greater than", r">", lambda*_:" is greater than "),
    Pattern("< to is less than", r"<", lambda*_:" is less than "),
    Pattern("= to equals", r"=", lambda*_:" equals "),
# ---------------------------------------------------------
    # abbreviations
    Pattern("ADHD", r"(?<![a-z\d])(ADHD)(?![a-z\d])", lambda*_:" A D H D "),
    Pattern("AFAIK", r"(?<![a-z\d])(AFAIK)(?![a-z\d])", lambda*_:" as far as I know "),
    Pattern("ADOFAI", r"(?<![a-z\d])(ADOFAI)(?![a-z\d])", lambda*_:" a dance of fire and ice "),
    Pattern("AKA", r"(?<![a-z\d])(AKA)(?![a-z\d])", lambda*_:" also known as "),
    Pattern("ASAP", r"(?<![a-z\d])(ASAP)(?![a-z\d])", lambda*_:" as soon as possible "),
    Pattern("ASL", r"(?<![a-z\d])(ASL)(?![a-z\d])", lambda*_:" American sign language "),
    Pattern("ASMR", r"(?<![a-z\d])(ASMR)(?![a-z\d])", lambda*_:" A S M R "),
    Pattern("BFF", r"(?<![a-z\d])(BFF)(?![a-z\d])", lambda*_:" best friends forever "),
    Pattern("BTW", r"(?<![a-z\d])(BTW)(?![a-z\d])", lambda*_:" by the way "),
    Pattern("FPS", r"(?<![a-z\d])(FPS)(?![a-z\d])", lambda*_:" frames per second "),
    Pattern("IIRC", r"(?<![a-z\d])(IIRC)(?![a-z\d])", lambda*_:" if I remember correctly "),
    Pattern("IMHO", r"(?<![a-z\d])(IMHO)(?![a-z\d])", lambda*_:" in my honest opinion "),
    Pattern("IMO", r"(?<![a-z\d])(IMO)(?![a-z\d])", lambda*_:" in my opinion "),
    Pattern("IRL", r"(?<![a-z\d])(IRL)(?![a-z\d])", lambda*_:" in real life "),
    Pattern("TIL", r"(?<![a-z\d])(TIL)(?![a-z\d])", lambda*_:" today I learned "),
    Pattern("TL;DR", r"(?<![a-z\d])(TL;?DR)(?![a-z\d])", lambda*_:" too long; didn't read "),
    Pattern("URL", r"(?<![a-z\d])(URL)(?![a-z\d])", lambda*_:" U R L "),
    Pattern("WIP", r"(?<![a-z\d])(WIP)(?![a-z\d])", lambda*_:" work in progress "),
    Pattern("YSK", r"(?<![a-z\d])(YSK)(?![a-z\d])", lambda*_:" you should know "),
# ---------------------------------------------------------
    Pattern("BMP", re.compile(r"(?<![a-z\d])(BMP)(?![a-z\d])",flags=re.I), lambda*_:" bitmap "),
    Pattern(".BMP", re.compile(r"(\.BMP)(?![a-z\d])",flags=re.I), lambda*_:" dot bitmap "),
    Pattern("CSS", re.compile(r"(?<![a-z\d])(CSS)(?![a-z\d])",flags=re.I), lambda*_:" C S S "),
    Pattern(".CSS", re.compile(r"(\.CSS)(?![a-z\d])",flags=re.I), lambda*_:" dot C S S "),
    Pattern("EXE", re.compile(r"(?<![a-z\d])(EXE)(?![a-z\d])",flags=re.I), lambda*_:" executable "),
    Pattern(".EXE", re.compile(r"(\.EXE)(?![a-z\d])",flags=re.I), lambda*_:" dot executable "),
    Pattern("JPG", re.compile(r"(?<![a-z\d])(JPE?G)(?![a-z\d])",flags=re.I), lambda*_:" J peg "),
    Pattern(".JPG", re.compile(r"(\.JPE?G)(?![a-z\d])",flags=re.I), lambda*_:" dot J peg "),
    Pattern("JSON", re.compile(r"(?<![a-z\d])(JSON)(?![a-z\d])",flags=re.I), lambda*_:" J son "),
    Pattern(".JSON", re.compile(r"(\.JSON)(?![a-z\d])",flags=re.I), lambda*_:" dot J son "),
    Pattern("GIF", re.compile(r"(?<![a-z\d])(GIF)(?![a-z\d])",flags=re.I), lambda*_:" gif "),
    Pattern(".GIF", re.compile(r"(\.GIF)(?![a-z\d])",flags=re.I), lambda*_:" dot gif "),
    Pattern("HTML", re.compile(r"(?<![a-z\d])(HTML)(?![a-z\d])",flags=re.I), lambda*_:" H T M L "),
    Pattern(".HTML", re.compile(r"(\.HTML)(?![a-z\d])",flags=re.I), lambda*_:" dot H T M L "),
    Pattern("MP3", re.compile(r"(?<![a-z\d])(MP3)(?![a-z\d])",flags=re.I), lambda*_:" M P three "),
    Pattern(".MP3", re.compile(r"(\.MP3)(?![a-z\d])",flags=re.I), lambda*_:" dot M P three "),
    Pattern("MP4", re.compile(r"(?<![a-z\d])(MP4)(?![a-z\d])",flags=re.I), lambda*_:" M P four "),
    Pattern(".MP4", re.compile(r"(\.MP4)(?![a-z\d])",flags=re.I), lambda*_:" dot M P four "),
    Pattern("PDF", re.compile(r"(?<![a-z\d])(PDF)(?![a-z\d])",flags=re.I), lambda*_:" P D F "),
    Pattern(".PDF", re.compile(r"(\.PDF)(?![a-z\d])",flags=re.I), lambda*_:" dot P D F "),
    Pattern("PNG", re.compile(r"(?<![a-z\d])(PNG)(?![a-z\d])",flags=re.I), lambda*_:" P N G "),
    Pattern(".PNG", re.compile(r"(\.PNG)(?![a-z\d])",flags=re.I), lambda*_:" dot P N G "),
    Pattern("PY", re.compile(r"(?<![a-z\d])(PY)(?![a-z\d])",flags=re.I), lambda*_:" python "),
    Pattern(".PY", re.compile(r"(\.PY)(?![a-z\d])",flags=re.I), lambda*_:" dot python "),
    Pattern("TXT", re.compile(r"(?<![a-z\d])(TXT)(?![a-z\d])",flags=re.I), lambda*_:" text "),
    Pattern(".TXT", re.compile(r"(\.TXT)(?![a-z\d])",flags=re.I), lambda*_:" dot text "),
    Pattern("WAV", re.compile(r"(?<![a-z\d])(WAV)(?![a-z\d])",flags=re.I), lambda*_:" wav "),
    Pattern(".WAV", re.compile(r"(\.WAV)(?![a-z\d])",flags=re.I), lambda*_:" dot wav "),
    Pattern("WEBP", re.compile(r"(?<![a-z\d])(WEBP)(?![a-z\d])",flags=re.I), lambda*_:" web P "),
    Pattern(".WEBP", re.compile(r"(\.WEBP)(?![a-z\d])",flags=re.I), lambda*_:" dot web P "),
    Pattern("ZIP", re.compile(r"(?<![a-z\d])(ZIP)(?![a-z\d])",flags=re.I), lambda*_:" zip "),
    Pattern(".ZIP", re.compile(r"(\.ZIP)(?![a-z\d])",flags=re.I), lambda*_:" dot zip "),

    Pattern("T", re.compile(r"(\.ZIP)(?![a-z\d])",flags=re.I), lambda*_:" dot zip "),
    # mc tf2
    # add gif by writing custom ipa, have valid word checker skip over
    Pattern("misc.", r"(?<![a-z\d])misc\.", lambda*_:" miscellaneous "),
    # BMP CSS EXE JPG JPEG JSON GIF HTML MP3 MP4 PDF PNG PY TXT WAV ZIP webp
    # URL C++
    Pattern("etc.", r"(?<![a-z\d])etc\.", lambda*_:" et cetera "),
    
    Pattern(".com", r"\.com(?![a-z])", lambda*_:" dot com "),
    Pattern(".org", r"\.org(?![a-z])", lambda*_:" dot org "),
    Pattern(".net", r"\.net(?![a-z])", lambda*_:" dot net "),
    Pattern(".edu", r"\.edu(?![a-z])", lambda*_:" dot E D U "),
    Pattern(".gov", r"\.gov(?![a-z])", lambda*_:" dot gov "),
    # make degrees into a function that checks for °[FCK]
    Pattern("°F", r"°F", lambda*_:" degrees fahrenheit "),
    Pattern("°C", r"°C", lambda*_:" degrees celsius "),
    Pattern("°K", r"°K", lambda*_:" degrees kelvin "),
    Pattern("°", r"°", lambda*_:" degrees "),

]


# specialGroupDict = Pattern.to_Patterns({
#     # for abbrevations instead of just space and teh beginning, look for:
#         # space, start of string, 
# })


unknownDict = Pattern.to_Patterns({
    "≥": " is greater than or equal to ",
    "≤": " is less than or equal to ",
    "≠": " does not equal ",
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


replacePatterns = unknownDict + longReplacePatterns



# def replace_patterns(text:str,patternList:list, originaltext=None) -> str:
#     if(not originaltext): originaltext = text 
#     newtext = text
#     for pattern in patternList:
#         search = re.search(pattern.reg,newtext)
#         if(search):
#             print(f"replaced \"{colors.color(search.group(),colors.bg.red)}\" with \"{colors.color(pattern.replFunc(newtext),colors.bg.blue)}\" using \"{pattern.desc}\"")
#             print(f"{pattern.colorsub(newtext,1)}")
#             newtext = pattern.sub(newtext,1)

#             newtext = replace_patterns(newtext, patternList, originaltext)[0]
#     return newtext, originaltext

thing = Replace("1111slkdjflka1as1lj232kf",[Pattern("1 to one", r"1", lambda*_:" one ")])
print(thing)
print(thing.patternList)
print(thing.ogtext)
print(thing.rep)


# write a tokenizer which labels which each value is
# like . would be pause.period
# ? would be pause.question
# hello would be word
# what's for dinner? would be a sentence. the ? would make it a question sentence