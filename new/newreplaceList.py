import re
from num2words import num2words
import unicodedata




class Pattern:
    def __init__(self, desc: str, reg: str, replFunc):
        self.desc = desc
        self.reg = reg
        self.replFunc = lambda text: replFunc(reg, text)

    def findall(self, text: str, flags=0):
        return re.findall(self.reg, text, flags)
    def sub(self, text: str, count: int = 0, flags=0) -> str:
        return re.sub(self.reg, self.replFunc(text), text, count, flags)

    def colorsub(self, text: str, count: int = 0, flags=0) -> str:
        # return f"{re.split(self.reg, text,1)[0]}{c.color(self.replFunc(text),c.bg.blue)}{re.split(self.reg, text,1)[-1]}"
        # array = re.split(self.reg,text)
        # return f"{array[0]}{colors.color(self.replFunc(text),colors.bg.blue)}{array[1]}"
        return re.sub(self.reg, colors.color(self.replFunc(text), colors.bg.blue), text, count, flags)

    def search(self, text, num=0, flags=0):
        return re.search(self.reg, text, flags)

    def group(self, text, num=0, flags=0):
        search = re.search(self.reg, text, flags)
        return search.group(num)

    def to_Patterns(dict: dict):
        array = []
        for defn in dict:
            value = dict[defn]
            array.append(
                Pattern(f"{defn} to {value}",
                    re.escape(defn),
                    lambda *_, val=value: val
                    )
            )
        return array

    class Replacing:
        def num2words(number, ordinal=False, lang='en', to='cardinal', **kwargs):
            "Num2words but without dashes"
            newn = num2words(number, ordinal, lang, to, **kwargs)
            return Pattern("remove dashes", r"-", lambda *_: " ").sub(newn)

        def time(reg: str, text: str):  # 1:32 3:00 am 12:63
            "Replaces valid times"
            num2words = Pattern.Replacing.num2words
            search = re.search(reg, text)
            parts = []
            parts.append(num2words(search.group(1)))
            if int(search.group(2)) < 10:
                parts.append("oh")
            if int(search.group(2)) == 0:
                parts.append("clock")
            if int(search.group(2)) != 0:
                parts.append(num2words(search.group(2)))
            if search.group(3):
                if   search.group(3).lower() == "am":
                    parts.append("A M")
                elif search.group(3).lower() == "pm":
                    parts.append("P M")
                # match search.group(3).lower():
                #     case "am": parts.append("A M")
                #     case "pm": parts.append("P M")
            return " " + " ".join(parts) + " "
        # can I use self.search?
        # class number:

        def ordinal_number(reg: str, text: str):
            "Replaces ordinal numbers like 1st 2nd 3rd"
            # num2words = Pattern.Replacing.num2words
            search = re.search(reg, text)
            parts = []
            parts.append(num2words(search.group()[:-2], False, "en", "ordinal"))
            return " " + " ".join(parts) + " "

        def currency(reg: str, text: str, currencySymbol="$"):
            "Replaces currencies"
            num2words = Pattern.Replacing.num2words
            search = re.search(reg, text)

            def find_plural(num: int, type: str, isdecimal: bool = False):
                names = {
                    "$": ["dollars", "dollar", "cents", "cent"],
                    "£": ["pounds", "pound", "pence", "penny"],
                    "€": ["euros",  "euro",  "cents", "cent"],
                    "¥": ["yen",    "yen",],
                    "¢": ["cents",  "cent",],
                }
                move = 0
                if (isdecimal):
                    move = 2
                if (int(num) == 1):
                    return names[type][move+1]
                else:
                    return names[type][move]
                # return {"plural": names[type][move], "singular": names[type][move+1]}
            parts = []
            # ["","two","dollars","thirteen","cents",""]
            # $£€¥¢
            if currencySymbol == "$" or currencySymbol == "£" or currencySymbol == "€":
                if (search.group(5)):            # .12 .00 exists
                    if (int(search.group(3)) == 0):    # 0.12, 0.00, 0.99
                        if (int(search.group(5)) == 0):    # 0.00
                            parts.append(num2words(0))
                            parts.append(find_plural(0, currencySymbol))
                        if (int(search.group(5)) > 0):     # 0.12, 0.99
                            parts.append(num2words(int(search.group(5))))
                            parts.append(find_plural(int(search.group(5)), currencySymbol, True))
                    if (int(search.group(3)) > 0):     # 1. 32. 1123.
                        parts.append(num2words(int(search.group(3))))
                        parts.append(find_plural(
                            int(search.group(3)), currencySymbol)+",")
                        # if(int(search.group(5))==0):    # 1.00 32.00 1123.00
                        if (int(search.group(5)) > 0):     # 1.12, 321.99
                            parts.append(num2words(int(search.group(5))))
                            parts.append(find_plural(int(search.group(5)), currencySymbol, True))
                else:                           # 1, 3, 1234, 0
                    if (int(search.group(3)) == 0):    # 0
                        parts.append(num2words(0))
                        parts.append(find_plural(0, currencySymbol))
                    if (int(search.group(3)) > 0):     # 1, 3, 1234
                        parts.append(num2words(int(search.group(3))))
                        parts.append(find_plural(int(search.group(3)), currencySymbol))
            elif currencySymbol == "¢" or currencySymbol == "¥":
                parts.append(num2words(int(search.group(2))))
                parts.append(find_plural(int(search.group(2)), currencySymbol))
            elif currencySymbol == "¢@":
                parts.append(num2words(int(search.group(1))))
                parts.append(find_plural(int(search.group(1)), "¢"))
            # parts = 
            return " " + " ".join(parts) + " "

        def phone_number(reg: str, text: str):
            "Replaces phone numbers"
            num2words = Pattern.Replacing.num2words
            search = re.search(reg, text)
            parts = []
            for part in re.findall(r"\d+", search.group()):
                parts.append(" ".join(map(num2words, re.findall(r"\d", part))))
            return " " + ", ".join(parts) + " "
            # search = re.search(reg,text)
            # return " " + " ".join(map(num2words,re.findall(r"\d",search.group()))) + " "

        def number(reg: str, text: str):
            "Replaces numbers to words"
            num2words = Pattern.Replacing.num2words
            search = re.search(reg, text)
            parts = ""
            if (float(search.group()) == 0):  # any number that's zero, 0, 0.00, .00
                parts = num2words(0, False, "en", "cardinal")
            else:                         # not = 0
                if (search.group(2)):  # (0).231, -(3).1, (3), (0)
                    if (int(search.group(2)) != 0):  # -(3).1, (3), -(4).32136, (5)
                        parts = num2words(float(search.group()), False, "en", "cardinal")
                        # parts[1] = num2words(0)
                    if (int(search.group(2)) == 0):  # -(0).1, (0).3213,
                        parts = "".join(num2words(float(search.group())).split("zero", 1))
            parts = Pattern("remove - from numbers", r"-", lambda *_: " ").sub(parts)
            # for part in parts:

            #     Pattern("remove - from numbers", r"-", lambda *_: " ").sub(part)

            return " " + parts + " "

        def file_extension(reg: str, text: str, repl: str):
            "Replaces phone numbers"
            search = re.search(reg, text)
            parts = ""
            if (search.group(1)):
                parts += " dot "
            parts += repl
            return parts


class Replace:
    def __init__(self, text: str, patternList: list):
        self.ogtext = text
        self.patternList = patternList
        self.rep = self.__replace_patterns(text, self.patternList)

    def __str__(self):
        return self.rep

    def __replace_patterns(self, text: str, patternList: list) -> str:
        newtext = text
        for pattern in patternList:
            search = re.search(pattern.reg, newtext)
            if (search):
                print(f"replaced \"{colors.color(search.group(),colors.bg.red)}\" with \"{colors.color(pattern.replFunc(newtext),colors.bg.blue)}\" using \"{pattern.desc}\"")
                print(f"{pattern.colorsub(newtext,1)}")
                newtext = pattern.sub(newtext, 1)
                newtext = self.__replace_patterns(newtext, patternList)
        return newtext

# Replace.__replace_patterns


periodDelimiters = (".", "!", "?", "\n", "\f", "\t", "\v")
commaDelimiters = (",", "~", "—", "(", ")", ":", ";")
spaceDelimiters = (" ", "-", "_", "/", "\\")
blankDelimiters = ("|",)
pauseDelimiters = periodDelimiters+commaDelimiters+spaceDelimiters+blankDelimiters
# use | to symbolize a nothing symbol

longReplacePatterns = [
    Pattern("remove _", r"_", lambda *_: " "),
    # ---------------------------------------------------------
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
            flags=re.I | re.X),# ignore case and whitespace
        lambda r, t: Pattern.Replacing.time(r, t)
    ),
    # ---------------------------------------------------------
    Pattern("commas in big numbers",
        r"\d{1,3}(,\d{3})+",
        lambda r, t: "".join(re.search(r, t).group().split(","))
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
            flags=re.I | re.X),# ignore case and whitespace
        lambda r, t: Pattern.Replacing.ordinal_number(r, t)
    ),
    # ---------------------------------------------------------
    # currency
    Pattern("$ to dollars",
        r"(\$)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda r, t: Pattern.Replacing.currency(r, t, "$")
    ),
    Pattern("£ to pounds",
        r"(£)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda r, t: Pattern.Replacing.currency(r, t, "£")
    ),
    Pattern("€ to euros",
        r"(€)((\d+)(\.(\d{2}))?)(?!\d)",
        lambda r, t: Pattern.Replacing.currency(r, t, "€")
    ),
    Pattern("¥ to yen",
        r"(¥)(\d+)",
        lambda r, t: Pattern.Replacing.currency(r, t, "¥")
    ),
    Pattern("¢ to cents",
        r"(¢)(\d+)",
        lambda r, t: Pattern.Replacing.currency(r, t, "¢")
    ),
    Pattern("¢ to cents reversed",
        r"(\d+)(¢)",
        lambda r, t: Pattern.Replacing.currency(r, t, "¢@")
    ),
    # ---------------------------------------------------------
    Pattern("phone numbers",
        r"(?<!\d)(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)",
        lambda r, t: Pattern.Replacing.phone_number(r, t)
    ),
    # ---------------------------------------------------------
    # "#" can be hashtag or number
    Pattern("# to \"hashtag\"",
        r"#(?! *\d *)",
        lambda *_: (" hashtag ")
    ),
    Pattern("# to \"number\"",
        r"#(?= *\d)",
        lambda *_: (" number ")
    ),
    # ---------------------------------------------------------
    # common characters
    Pattern("@ to at", r"@", lambda *_: " at "),
    Pattern("% to percent", r"%", lambda *_: " percent "),
    Pattern("& to and", r"&", lambda *_: " and "),
    Pattern("* to asterisk", r"\*", lambda *_: " asterisk "),
    Pattern("+ to plus", r"\+", lambda *_: " plus "),
    Pattern("> to is greater than", r">", lambda *_: " is greater than "),
    Pattern("< to is less than", r"<", lambda *_: " is less than "),
    Pattern("= to equals", r"=", lambda *_: " equals "),
    # ---------------------------------------------------------
    # abbreviations
    Pattern("24/7", r"(?<!\w)(24/7)(?!\w)", lambda *_: " 24 7 "),
    Pattern("ADHD", r"(?<!\w)(ADHD|Adhd|adhd)(?!\w)", lambda *_: " A|D|H|D "),  # a is pronounced uh
    Pattern("AFAIK", r"(?<!\w)(AFAIK|Afaik|afaik)(?!\w)", lambda *_: " as far as I know "),
    Pattern("AFK", r"(?<!\w)(AFK|Afk|afk)(?!\w)", lambda *_: " as far as I know "),
    Pattern("ADOFAI", r"(?<!\w)(ADOFAI|Adofai|adofai)(?!\w)", lambda *_: " a dance of fire and ice "),
    Pattern("AKA", r"(?<!\w)(AKA|aka|Aka)(?!\w)", lambda *_: " also known as "),
    Pattern("API", r"(?<!\w)(API)(?!\w)", lambda *_: " A|P|I "),
    Pattern("ASAP", r"(?<!\w)(ASAP|asap)(?!\w)", lambda *_: " as soon as possible "),
    Pattern("ASL", r"(?<!\w)(ASL)(?!\w)", lambda *_: " American sign language "),
    Pattern("ASMR", r"(?<!\w)(ASMR)(?!\w)", lambda *_: " A|S|M|R "),
    Pattern("ATM", r"(?<!\w)(ATM)(?!\w)", lambda *_: " A|T|M "),
    Pattern("B4", r"(?<!\w)(B4|b4)(?!\w)", lambda *_: " before "),
    # Pattern("BC", r"(?<!\w)(BC|Bc|bc)(?!\w)", lambda *_: " because "),
    Pattern("BF", r"(?<!\w)(BF|Bf|bf)(?!\w)", lambda *_: " boyfriend "),
    Pattern("BFF", r"(?<!\w)(BFF|Bff|bff)(?!\w)", lambda *_: " best friends forever "),
    Pattern("BRB", r"(?<!\w)(BRB|Brb|brb)(?!\w)", lambda *_: " be right back "),
    Pattern("BTW", r"(?<!\w)(BTW|Btw|btw)(?!\w)", lambda *_: " by the way "),
    Pattern("C U L8R", r"(?<!\w)((C\ U|C\ u|c\ u) (L8R|l8r))(?!\w)", lambda *_: " see you L8R "),
    Pattern("CEO", r"(?<!\w)(CEO)(?!\w)", lambda *_: " C|E|O "),
    Pattern("DND", r"(?<!\w)(DND|Dnd|dnd)(?!\w)", lambda *_: " D N D "),
    Pattern("FAQ", r"(?<!\w)(FAQ)(?!\w)", lambda *_: " frequently asked questions "),
    Pattern("FPS", r"(?<!\w)(FPS)(?!\w)", lambda *_: " frames per second "),
    Pattern("FR", r"(?<!\w)(FR|Fr|fr)(?!\w)", lambda *_: " for real "),
    Pattern("FRFR", r"(?<!\w)(FRFR|Frfr|frfr)(?!\w)", lambda *_: " for real for real "),
    Pattern("FYI", r"(?<!\w)(FYI|Fyi|fyi)(?!\w)", lambda *_: " F|Y|I "),
    Pattern("GF", r"(?<!\w)(GF|Gf|gf)(?!\w)", lambda *_: " girlfriend "),
    Pattern("GG", r"(?<!\w)(GG|Gg|gg)(?!\w)", lambda *_: " G|G "),
    Pattern("GOAT", r"(?<!\w)(GOAT)(?!\w)", lambda *_: " greatest of all time "),
    Pattern("GN", r"(?<!\w)(GN|Gn|gn)(?!\w)", lambda *_: " goodnight "),
    Pattern("GTG/G2G", r"(?<!\w)(GTG|G2G|G2g|g2g)(?!\w)", lambda *_: " got to go "),
    Pattern("H8", r"(?<!\w)(H8|h8)(?!\w)", lambda *_: " hate "),
    Pattern("HIV", r"(?<!\w)(HIV)(?!\w)", lambda *_: " H|I|V "),
    Pattern("HQ", r"(?<!\w)(HQ|Hq|hq)(?!\w)", lambda *_: " H|Q "),
    Pattern("IDC", r"(?<!\w)(IDC|Idc|idc)(?!\w)", lambda *_: " I don't care "),
    Pattern("IDK", r"(?<!\w)(IDK|Idk|idk)(?!\w)", lambda *_: " I don't know "),
    Pattern("IDGAF", r"(?<!\w)(IDGAF|Idgaf|idgaf)(?!\w)", lambda *_: " I don't give a fuck "),
    Pattern("IIRC", r"(?<!\w)(IIRC|Iirc|iirc)(?!\w)", lambda *_: " if I remember correctly "),
    Pattern("IKR", r"(?<!\w)((IKR|Ikr|ikr)\??)(?!\w)", lambda *_: " I know right? "),
    Pattern("ILY", r"(?<!\w)(ILY|Ily|ily)(?!\w)", lambda *_: " I love you "),
    Pattern("ILYSM", r"(?<!\w)(ILYSM|Ilysm|ilysm)(?!\w)", lambda *_: " I love you so much "),
    Pattern("IMHO", r"(?<!\w)(IMHO|Imho|imho)(?!\w)", lambda *_: " in my honest opinion "),
    Pattern("IMO", r"(?<!\w)(IMO|Imo|imo)(?!\w)", lambda *_: " in my opinion "),
    Pattern("IRL", r"(?<!\w)(IRL|Irl|irl)(?!\w)", lambda *_: " in real life "),
    Pattern("IYKYK", r"(?<!\w)(IYKYK|Iykyk|iykyk)(?!\w)", lambda *_: " if you know you know "),
    Pattern("JK", r"(?<!\w)(JK|Jk|jk)(?!\w)", lambda *_: " just kidding "),
    Pattern("KYS", r"(?<!\w)(KYS|Kys|kys)(?!\w)", lambda *_: " kill yourself "),
    Pattern("L8R", r"(?<!\w)(L8R|L8r|l8r)(?!\w)", lambda *_: " later "),
    # Pattern("LMAO", r"(?<!\w)(LMF?AO|Lmf?ao|lmf?ao)(?!\w)", lambda*_:" l "), # custom pronounce
    Pattern("LMK", r"(?<!\w)(LMK|Lmk|lmk)(?!\w)", lambda *_: " let me know "),
    # Pattern("LOL", r"(?<!\w)(LOL|Lol|lol)(?!\w)", lambda*_:" l "), # custom
    # Pattern("NASA", r"(?<!\w)(NASA|Nasa|nasa)(?!\w)", lambda*_:"  "), # custom
    Pattern("M8TE", r"(?<!\w)(M8TE|M8te|m8te)(?!\w)", lambda *_: " mate "),
    Pattern("NGL", r"(?<!\w)(NGL|Ngl|ngl)(?!\w)", lambda *_: " not gonna lie "),
    Pattern("NVM", r"(?<!\w)(NVM|Nvm|nvm)(?!\w)", lambda *_: " nevermind "),
    Pattern("OBV", r"(?<!\w)(OBV|Obv|obv)(?!\w)", lambda *_: " obviously "),
    Pattern("OG", r"(?<!\w)(OG|Og|og)(?!\w)", lambda *_: " Oh G "),
    Pattern("OMG", r"(?<!\w)(OMG|Omg|omg)(?!\w)", lambda *_: " Oh M G "),
    Pattern("PEMDAS", r"(?<!\w)(PEMDAS|Pemdas|pemdas)(?!\w)", lambda *_: " pem|dass "),
    Pattern("POV", r"(?<!\w)(POV|Pov|pov)(?!\w)", lambda *_: " point of view "),
    Pattern("PTSD", r"(?<!\w)(PTSD|Ptsd|ptsd)(?!\w)", lambda *_: " P|T|S|D "),
    Pattern("RN", r"(?<!\w)(RN|Rn|rn)(?!\w)", lambda *_: " right now "),
    Pattern("ROTFLOL", r"(?<!\w)(ROTFLOL|Rotflol|rotflol)(?!\w)", lambda *_: " rolling on the floor laughing out loud "),
    Pattern("ROTFL", r"(?<!\w)(ROTFL|Rotfl|rotfl)(?!\w)", lambda *_: " rolling on the floor laughing "),
    Pattern("SMH", r"(?<!\w)(SMH|Smh|smh)(?!\w)", lambda *_: " S|M|H my head "),
    Pattern("STFU", r"(?<!\w)(STFU|Stfu|stfu)(?!\w)", lambda *_: " shut the fuck up "),
    Pattern("TBA", r"(?<!\w)(TBA|Tba|tba)(?!\w)", lambda *_: " to be announced "),
    Pattern("TBD", r"(?<!\w)(TBD|Tbd|tbd)(?!\w)", lambda *_: " to be determined "),
    Pattern("TBF", r"(?<!\w)(TBF|Tbf|tbf)(?!\w)", lambda *_: " to be fair "),
    Pattern("TIL", r"(?<!\w)(TIL)(?!\w)", lambda *_: " today I learned "),
    Pattern("TL;DR", r"(?<!\w)(TL;?DR|Tl;?dr|tl;?dr)(?!\w)", lambda *_: " too long; didn't read "),
    Pattern("TTYL", r"(?<!\w)(TTYL|Ttyl|ttyl)(?!\w)", lambda *_: " talk to you later "),
    Pattern("TMI", r"(?<!\w)(TMI|Tmi|tmi)(?!\w)", lambda *_: " too much information "),
    Pattern("TYSM", r"(?<!\w)(TYSM|Tysm|tysm)(?!\w)", lambda *_: " thank you so much "),
    Pattern("URL", r"(?<!\w)(URL|Url|url)(?!\w)", lambda *_: " U|R|L "),
    Pattern("URLs", r"(?<!\w)(URL|Url|url)(S|s)(?!\w)", lambda *_: " U|R|L|S "),  # custom
    Pattern("VIP", r"(?<!\w)(VIP)(?!\w)", lambda *_: " V|I|P "),
    Pattern("VIPs", r"(?<!\w)(VIP)(S|s)(?!\w)", lambda *_: " V|I|Pees "),  # custom
    Pattern("WIP", r"(?<!\w)(WIP)(?!\w)", lambda *_: " work in progress "),
    Pattern("WTF", r"(?<!\w)(WTF|Wtf|wtf)(?!\w)", lambda *_: " what the fuck "),
    Pattern("WYD", r"(?<!\w)(WYD|Wyd|wyd)(?!\w)", lambda *_: " what you doing? "),
    Pattern("W/", r"(?<!\w)(W/|w/)", lambda *_: " with "),
    Pattern("W/O", r"(?<!\w)(W/O|W/o|w/o)(?!\w)", lambda *_: " without "),
    Pattern("XOXO", re.compile(r"(?<![a-z\d])(XOXO)(?![a-z\d])", flags=re.I), lambda *_: " hugs and kisses "),
    Pattern("YOLO", r"(?<!\w)(YOLO|Yolo|yolo)(?!\w)", lambda *_: " yo|low "),
    Pattern("YSK", r"(?<!\w)(YSK)(?!\w)", lambda *_: " you should know "),
    # ---------------------------------------------------------
    Pattern("C++", r"((?<!\w)|\.)(C|c)\+\+(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " C plus plus ")),
    Pattern("C#", r"((?<!\w)|\.)(C)#(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " C sharp ")),
    Pattern("CSS", r"((?<!\w)|\.)(CSS|Css|css)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " C|S|S ")),
    Pattern("EXE", r"((?<!\w)|\.)(EXE|Exe|exe)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " E|X|E ")),
    Pattern("JPG", r"((?<!\w)|\.)(JPE?G|Jpe?g|JPe?g|jpe?g)(?!\w)",lambda r, t: Pattern.Replacing.file_extension(r, t, " J|peg ")),
    Pattern("JPGs", r"((?<!\w)|\.)(JPE?G|Jpe?g|JPe?g|jpe?g)(S|s)(?!\w)",lambda r, t: Pattern.Replacing.file_extension(r, t, " J|pegs ")),
    Pattern("JSON", r"((?<!\w)|\.)(JSON|Json|json)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " J|son ")),
    # Pattern("GIF", r"((?<!\w)|\.)(GIF|Gif|gif)(?!\w)", lambda r, t: Pattern.Replacing.file_extension(r, t, " gif ")),  # not in ipa, neither is plain gif word
    # Pattern("GIFs", r"((?<!\w)|\.)(GIF|Gif|gif)(S|s)(?!\w)", lambda r, t: Pattern.Replacing.file_extension(r, t, " gifs ")),  # not in ipa, neither is plain gif word
    Pattern("HTML", r"((?<!\w)|\.)(HTML|Html|html)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " H|T|M|L ")),
    Pattern("MP3", r"((?<!\w)|\.)(MP3|Mp3|mp3)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " M|P|3 ")),
    Pattern("MP3s", r"((?<!\w)|\.)(MP3|Mp3|mp3)(S|s)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " M|P|3|s ")),  # custom
    Pattern("MP4", r"((?<!\w)|\.)(MP4|Mp4|mp4)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " M|P|4 ")),
    Pattern("MP4s", r"((?<!\w)|\.)(MP4|Mp4|mp4)(S|s)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " M|P|4|s ")),  # custom
    Pattern("PDF", r"((?<!\w)|\.)(PDF|Pdf|pdf)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " P|D|F ")),
    Pattern("PDFs", r"((?<!\w)|\.)(PDF|Pdf|pdf)(S|s)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " P|D|F|s ")),
    Pattern("PNG", r"((?<!\w)|\.)(PNG|Png|png)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " P|N|G ")),
    Pattern("PNGs", r"((?<!\w)|\.)(PNG|Png|png)(S|s)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " P|N|G|s ")),
    # Pattern("WAV", r"((?<!\w)|\.)(WAV|Wav|wav)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " wav ")),  # not in ipa
    Pattern("WEBP", r"((?<!\w)|\.)(WEBP|WebP|Webp|webp)(?!\w)",lambda r, t: Pattern.Replacing.file_extension(r, t, " web|P ")),
    Pattern("ZIP", r"(\.)(ZIP|Zip|zip)(?!\w)", lambda r,t: Pattern.Replacing.file_extension(r, t, " dot zip ")),

    # mc tf2
    # add gif by writing custom ipa, have valid word checker skip over
    # ---------------------------------------------------------
    Pattern("i.e.", r"(?<!\w)(i\.e|I\.E)\.", lambda *_: " that is, "),
    Pattern("e.g.", r"(?<!\w)(e\.g|E\.G)\.", lambda *_: " for example, "),
    Pattern("misc.", r"(?<!\w)misc\.", lambda *_: " miscellaneous "),
    Pattern("etc.", r"(?<!\w)etc\.", lambda *_: " et cetera "),
    # ---------------------------------------------------------
    Pattern(".com", r"\.com(?!\w)", lambda *_: " dot com "),
    Pattern(".org", r"\.org(?!\w)", lambda *_: " dot org "),
    Pattern(".net", r"\.net(?!\w)", lambda *_: " dot net "),
    Pattern(".edu", r"\.edu(?!\w)", lambda *_: " dot E|D|U "),
    Pattern(".gov", r"\.gov(?!\w)", lambda *_: " dot gov "),
    # make degrees into a function that checks for °[FCK]
    Pattern("°F", r"°F", lambda *_: " degrees fahrenheit "),
    Pattern("°C", r"°C", lambda *_: " degrees celsius "),
    Pattern("°K", r"°K", lambda *_: " degrees kelvin "),
    Pattern("°", r"°", lambda *_: " degrees "),
    # ---------------------------------------------------------
    # numbers, can be negative or have decimal
    Pattern("numbers",  # this should go after mp3
        r"-?((\d+)(\.(\d+))?|(\.(\d+)))",
        lambda r, t: Pattern.Replacing.number(r, t)
    ),
    # dont forget multiple points 12.43.5
    # ([0-9]+)(\.[0-9]+)+
    # numbers with decimals, 12.34


]


# specialGroupDict = Pattern.to_Patterns({
#     # for abbrevations instead of just space and teh beginning, look for:
#         # space, start of string,
# })

    
unknownDict = Pattern.to_Patterns({
    # "|": " ",

    "≥": " >= ",
    "≤": " <= ",
    "≠": " != ",
    "±": " + or - ",
    "∞": " infinity ",
    "π": " pi ", # these should all be in a different group

    "…": ".", # this should be in a different group
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

    "Ñ": "ny", # these should be in a different group
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

    "Ø": "oo", # these should be in a different group
    "ø": "oo",

    "ₚ": "p",

    "ₛ": "s",
    "Š": "s",
    "š": "s",

    "ß": "ss", # these should be in a different group
    "ẞ": "ss",

    "ₜ": "t",

    "Ð": "th", # these should be in a different group
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



    "½": " 1 half ", # these should all be in a different group
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

    "↑": " up ", # these should all be in a different group
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

thing = Replace("1111slkdjflka1as1lj232kf", [Pattern("1 to one", r"1", lambda *_: " one ")])
print(thing)
print(thing.patternList)
print(thing.ogtext)
print(thing.rep)


# write a tokenizer which labels which each value is
# like . would be pause.period
# ? would be pause.question
# hello would be word
# what's for dinner? would be a sentence. the ? would make it a question sentence


# more odd characters:


# if there's a ¡ or ¿ then try to detect in between as a sentence

# add url interpreter