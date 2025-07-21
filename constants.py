import re
from contextlib import suppress
from num2words import num2words


# periodPauseDelimiters = ".!&?\n"
# commaPauseDelimiters  = ",~*()=+\\:;\""
# spacePauseDelimiters  = " -_></"
periodPauseDelimiters = [".","!","?","\n"]
commaPauseDelimiters = [",","~","—","(",")",":",";"]
spacePauseDelimiters = [" ","-","_","/","\\"]
pauseDelimiters = periodPauseDelimiters + commaPauseDelimiters + spacePauseDelimiters
# print(pauseDelimiters)

# class Pause:
#     def __init__(self):
#         # self.
#         pass

specialGroupDict = {
    " misc.": " miscellaneous",
    " etc.": " et cetera",
    ".com": " dot com",
    ".org": " dot org",
    ".net": " dot net",
    ".edu": " dot ee dee you",
    ".gov": " dot guv",
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
    "°F": " degrees fahrenheit ",
    "°C": " degrees celsius ",
}

replacePatterns = [
    # takes care of am or pm
    [r"(?i)((?<=(?<!\d)[1-9]:[0-5][0-9])|(?<=(?<!\d)1[0-2]:[0-5][0-9])) *am(?![a-z])",
        lambda x: " ay em "
    ],
    [r"(?i)((?<=(?<!\d)[1-9]:[0-5][0-9])|(?<=(?<!\d)1[0-2]:[0-5][0-9])) *pm(?![a-z])",
        lambda x: " pee em "
    ],
    # times that end in 00
    # needs to select and replace :00 with " oh clock "
    # [r"((?<=[1-9])|(?<=\D1[0-2])):[0-5][0-9]( ?(?![a-zA-Z0-9]))/i",
    #     lambda x:(
    #         num2words(re.search(r"([1-9]|1[0-2])+?(?=:)",x).group())
    #         + " oh clock "
    #     )            
    # ],
    # times that end in 04 like 12:04 or 3:07
    # needs to select and replace :0 with " oh "
    # [r"([1-9]|1[0-2]):(0[1-9])",
    #     lambda x:(
    #         num2words(re.search(r"([1-9]|1[0-2])+?(?=:)",x).group())
    #         + " oh "
    #         + num2words(re.search(r"(?<=:0)([1-9])",x).group())
    #     )            
    # ],
    # all other valid times
    # selects the : in a time
    # [r"([1-9]|1[0-2]):([1-5][0-9]|[1-5][1-9])",
    #     lambda x:(
    #         num2words(re.search(r"([1-9]|1[0-2])+?(?=:)",x).group())
    #         + " "
    #         + num2words(re.search(r"(?<=:)([1-5][0-9]|[0-5][1-9])",x).group())
    #     )            
    # ],
    # dash minus
    [r"-(?=[0-9])+",
        lambda x:(
            (" minus " if re.search(r"(?<=-)[0-9]+",x).group() else "")
        )            
    ],
    # decimals, make the . in 13.35 or in 13.35.47.57 to dot
    [r"(?<=[0-9])+\.(?=[0-9])+",
        lambda x:(
            # (" minus " if re.search(r"[0-9]+(?=\.)",x).group() else "")
            (" point " if re.search(r"(?<=[0-9])\.(?=[0-9])",x) else " ")
        )
    ],
    # ([0-9]+)(\.[0-9]+)+
    # numbers with decimals, 12.34
    # negative numbers -1123.45
        # but not using - as minus like this 123-324
    # multiple points 12.43.5
    # x = [n for n in range(10)]

    # ------------

    # prices: the symbol is pronounced before
    
    # "$": " dollar ",
    # $400.23: 400 dollars and 23 cents
    # $3: 3 dollars
    #

    # "£": " pound ",
    # "€": " euro ",
    # "¥": " yen ",
    # cent is the only one that goes before
    # "¢": " cent ",

]




# qwerty = "I go to the mall at 4:32 pm after work"
# print(
#     map(
#         x[1],
#         re.sub(x[0], x[1](qwerty), qwerty) if(re.search(x[0],qwerty))
#         ) for x in replaceTime
#     )

# for what in replaceTime:
#     if(re.search(what[0],qwerty)): print(re.sub(what[0], what[1](qwerty), qwerty))




unknownDict = {
    "@": " at ",
    "#": " hashtag ",
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

    
    "°": " degrees ",
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
    "Ç": "s",
    "ç": "s",
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
}


testtext = "come @ me b1ro #gamer 100% m&m gimme a yummy ^"