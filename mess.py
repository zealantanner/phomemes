import re
import eng_to_ipa as ipa
import num2words
from unidecode import unidecode
from Qualities import colors


class SortedList(list):
    def __init__(self, *args, reverse=False, **kwargs):
        super().__init__(*args, **kwargs)       # Initialize the super class
        self.reverse = reverse
        self.sort(reverse=self.reverse)         # Do additional things with the custom keyword arguments





class Token:
    def __init__(self, text:str, span:tuple[int,int], asif=None):
        self.text = text
        self.span = span
        self.asif = text if asif is None else asif
    def __str__(self):
        return self.text

class Word(Token):
    type IPA = str #> custom type for IPA
    def __init__(self, text:str, span:tuple[int,int], asif=None, pronounce:IPA=None):
        super().__init__(text, span, asif)
        if type == "acronym": pass
        #> pronunciation override
        
class Delimiter(Token):
    def __init__(self, text:str, span:tuple[int,int], asif=None, type=None):
        super().__init__(text, span, asif)

class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data
    def add_child(self, child):
        "Creates parent-child relationship"
        print("Adding ", child)
        self.children.append(child)        
    def traverse(self):
        "Moves through each node referenced from self downwards"
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop()
            print(current_node.data)
            nodes_to_visit += current_node.children

class Set(Tree):
    def __init__(self, text:str, span:tuple, convertby=None):
        super().__init__(text)
        self.text = text
        self.span = span
        self.convertby = convertby
        # ratio   = r"(?<first>\d+)(:)(?<second>\d+)"
        class reg:
            space   = r" "
            period  = r"\."
            number  = r"^\d+$"
            word    = r"^\w+$"
        

        # m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
        # # m.group('last_name')
        # parts
        if(re.search(reg.space, text)):
            result = re.search(reg.space, text)
            start = text[:result.start()]
            middle = text[result.start():result.end()]
            end = text[result.end():]
            if start != "":
                self.add_child(Set(start,(self.span[0],result.start())))
            self.add_child(Delimiter(" ",(result.start(),result.end())))
            if end != "":
                self.add_child(Set(end,(result.end(),self.span[1])))
                
        elif(re.search(reg.period, text)):
            result = re.search(reg.period, text)
            start = text[:result.start()]
            middle = text[result.start():result.end()]
            end = text[result.end():]
            if start != "":
                self.add_child(Set(start,(self.span[0],result.start())))
            self.add_child(Delimiter(".",(result.start(),result.end())))
            if end != "":
                self.add_child(Set(end,(result.end(),self.span[1])))
        elif(re.search(reg.word, text)):
            result = re.search(reg.word, text)
            middle = text[result.start():result.end()]
            self.add_child(Word(middle,(result.start(),result.end())))
        else:
            raise ValueError(f"{text}\ncouldn't be helped")



        # self.children = [
        #     Set(text[:result.start()],),
        #     Delimiter(text[result.start():result.end()])
        # ]
        # match convertby:
        #     case None:
        #     case "spaces":
        # self.set_children(
        #     # Set("the bomb", (0,8)),
        #     Delimiter(".", (8,9)),
        #     Word("com", (9,12)),

        # )

    # class Reg:
        
    # def _split(self, text:str, span:tuple):
    #     for 
    def __str__(self):
        return self.text

class Split:
    def __init__(self, regex, func):
        pass
    def num2words():pass
    def phone_number():pass
    def currency():pass

class Sentence(Set):
    def __init__(self, text):
        #> function for removing whitespace on sides and unidecode
        super().__init__(text, (0,len(text)))





radthing = Word("$",(0,1), asif="dollars", type="symbol")
print(radthing.asif)



coolthing = Sentence("apple bee and me.com")
coolthing.traverse()
print(f"span {coolthing.span}")
print(f"text {coolthing.text}")
# print(f"type {coolthing.type}")
print(f"data {coolthing.data}")



spacereg = "ee a"
# result = re.match(spacereg,coolthing.text)
# print(result)
# result = re.compile(spacereg,coolthing.text)
# print(result)
result = re.search(spacereg,coolthing.text)
print(result.span())
print(coolthing.text[:result.start()])
print(coolthing.text[result.start():result.end()])
print(coolthing.text[result.end():])

# "patternfinder"


sometext = Sentence("apple and bees") 
# print(sometext.)
# sometext.


# m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
# m.group('first_name')
# m.group('last_name')

# class Convert:
#     def __init__(self, name:str, desc:str, patt, func):
#         self.name = name
#         self.desc = desc
#         self.patt = patt
#         self.func = func
#     def find():
#         return 
#     class Str:
#         def num2words(number, ordinal=False, lang='en', to='cardinal', **kwargs):
#             "Num2words but without dashes"
#             newn = num2words(number, ordinal, lang, to, **kwargs)
#             return Pattern("remove dashes", r"-", lambda *_: " ").sub(newn)
#     # class Setify:
#     #     def 
#     #     pass
#     #     # class:
#     # class Tokenify









# thingy = str("tree", "map")
# print(thingy)

# class Set(str):
#     # def __init__(self, text:list[str], tags = None):
#     def __init__(self, text:str, tags = None):
#         self.text = text
#         self.tags = tags
#     class Convert:
#         def default(text:str, position:list[int,int] = None):
#             "nonspecific set converter"
#             search = re.search(reg, text)
#         def num2words(self,aSet):
#             return Set()
#         def phone_number(text:str, reg: str):
#             "Replaces phone numbers"
#             num2words = Pattern.Replacing.num2words
#             search = re.search(reg, text)
#             parts = []
#             for part in re.findall(r"\d+", search.group()):
#                 parts.append(" ".join(map(num2words, re.findall(r"\d", part))))
#             return " " + ", ".join(parts) + " "
#     # Pattern("$ to dollars",
#     #     r"(\$)((\d+)(\.(\d{2}))?)(?!\d)",
#     #     lambda r, t: Pattern.Replacing.currency(r, t, "$")
#     # ),
#         # def to_word(val):
#         #     return Word(val)
#         # def to_delimiter(val):
#         #     return 
#     def tokenize(self):
#         if issubclass(type(self.text),Set):
#             return self.text
#         if isinstance(self.text[0], list):
#             return Set.tokenize(self.text[0]) + Set.tokenize(self.text[1:])
#         return self.text[:1] + Set.tokenize(self.text[1:])
    
# print(Set("the text").tokenize())

# class Sentence(Set):
#     # def __init__(self, text:str, type: list[str] = None):
#     #     self.text = text,
#     # def __init__(self, text, tags = None):
#     #     super().__init__(text, tags)
#     # def convert_to_sets()
#     #     self.text
#     #     return 
#     pass

# Sentence("   I want $7.05") ->
# [
#   Set("I want $7.05", (0,11)) ->
#   [
# 	Set("I want ",  	(0, 6)), ->
# 	[
#   	Word("I",       	(0, 0)),
#   	Delimiter(" ",  	(1, 1)),
#   	Word("want",    	(2, 5)),
#   	Delimiter(" ",  	(6, 6)),
# 	]
# 	Set("$7.05",    	(7,11),  convertby="currency"), ->
# 	[
#   	Set("7",        	(8, 8),  convertby="num2words"), ->
#   	[
#     	Word("7",       	(8, 8),  asif="seven")),
#   	]
#   	Delimiter(),
#   	Word("$",       	(7, 7),  asif="dollars"),
#   	Delimiter(".",  	(9, 9),  asif=" "),
#   	Word("",                 	 asif="and"),
#   	Delimiter(),
#   	Set("05",       	(10,11), convertby="num2words"), ->
#   	[
#     	Word("05",      	(10,11), asif="five"),
#   	]
#   	Delimiter(),
#   	Word("",                 	asif="cents"),
# 	]
#   ]
# ]







# example = Sentence("it is 7:00")
# example.convert_to_tokens()
# # output:
# []


# Set("7").Word("seven")


# class Token:
#     def __init__(self, text, convertby=None):
#         pass
#     def tokenize(self):
#         if issubclass(type(self.text),Token):
#             return self.text
#         if isinstance(self.text[0], list):
#             return Set.tokenize(self.text[0]) + Set.tokenize(self.text[1:])
#         return self.text[:1] + Set.tokenize(self.text[1:])

# class Word(Token):
#     pass
# class Delimiter(Token):
#     pass

# print(Token("the text").tokenize())



# class Thing:


# class Textify:
#     def __init__(self, text):
#         self.text = text
#         # self.repl = 
#         # self.
#     def __str__(self):
#         return self.text
    

# # class Jank(Obby):


# thing1 = Textify("qwe")
# thing2 = Textify("rty")
# thing3 = Textify("uio")
# thing4 = Textify("p[]")

# thing = Textify("johñny ôwes me £1.34")

# customCharacterConverter


# print(unidecode("""
#                 kožušček johñny ôwes me £1.34
#                 st 3rd % 3:59 Pm 3:09 pm 3:59 °F $1,000.10 ¢
#                 "$": ["dollars", "dollar", "cents", "cent"],
#                     "£": ["pounds", "pound", "pence", "penny"],
#                     "€": ["euros",  "euro",  "cents", "cent"],
#                     "¥": ["yen",    "yen",],
#                     "¢": ["cents",  "cent",],
#                  "≥": " >= ",
# """))

checklist = "½⅓¼⅕⅙⅐⅛⅑⅒⅔⅖¾⅗⅜⅘⅚⅝⅞↑↓←→≥≤≠±∞π\n\f\t\v"

# which1000 = 4
# for i in range(1000*(which1000-1),1000*which1000):
#     char = chr(i)
#     if(unidecode(char) != char):
#         print(f"{i}:\t{colors.color(char,colors.bg.blue)}\t{colors.color(unidecode(char),colors.bg.red)}\t{list(map((lambda x: f"{unidecode(x)}: {ord(x)}"), unidecode(char)))}")

# for char in checklist:
#     if(unidecode(char) != char):
#         print(f"{ord(char)}: {colors.color(char,colors.bg.blue)}\t{colors.color(unidecode(char),colors.bg.red)}")

# print(unidecode("£45.32, at 12:34 pm for Zealañ."))




# thing = Textify("Zealañ ôwes me $1.34")
# thing = Sentence[
#           Token(text:"Zealañ", translated:"Zealan")
#       ]

# ----------------------------------------
# Sentence("£45.32, at 12:34 pm for Zealañ.")
# ----------------------------------------
# Sentence("£45.32, at 12:34 pm for Zealan.") -- custom unidecode ignores list of characters, £ for example
# ----------------------------------------
#   Set("£45.32",       (0, 5)),
#   Set(", at ",        (6, 10)),
#   Set("12:34 pm",     (11,18)),
#   Set(" for Zealan.", (19,30)),
# ---------------------------------------- do this part differaently actually, should be like below
#   Set("£45.32",       (0, 5)),
#   Delimiter(", ",     (6, 7)),
#   Set("at",           (8, 9)),
#   Delimiter(" ",      (10,10)),
#   Set("12:34 pm",     (11,18)),
#   Delimiter(" ",      (19,19)),
#   Set("for",          (20,22)),
#   Delimiter(" ",      (23,23)),
#   Set("Zealan",       (24,29)),
#   Delimiter(".",      (30,30)),
# ----------------------------------------
#   Set("£45.32",               (0, 5)),    translated with currency function
#       Set("45",               (1, 2)),    translated with num2words
#           Word("forty",       (1, 1)),
#           Delimiter(" "),
#           Word("five",        (2, 2)),
#       ),
#       Delimiter(" "),
#       Word("pounds",          (0, 0)),
#       Delimiter(" ",          (3, 3)),
#       Set("32",               (4, 5)),    translated with num2words
#           Word("thirty",      (4, 4)),
#           Delimiter(" "),
#           Word("two",         (5, 5)),
#       ),
#       Delimiter(" "),
#       Word("pence"),
#   ),
#   Delimiter(", ",             (6, 7)),
#   Word("at",                  (8, 9)),
#   Delimiter(" ",              (10,10)),
#   Set("12:34 pm",             (11,18)),   translated with clock time function
#       Set("12",               (11,12)),   translated with num2words
#           Word("twelve",      (11,12)),
#       ),
#       Delimiter(":",          (13,13)),
#       Set("34",               (14,15)),   translated with num2words
#           Word("thirty",      (14,14)),
#           Delimiter(" "),
#           Word("four",        (15,15)),
#       ),
#       Delimiter(" ",          (16,16)),
#       Word("p"),              (17,17), "pi"),
#       Word("m"),              (18,18), "ɛm"),
#   ),
#   Delimiter(" ",              (19,19)),
#   Word("for",                 (20,22)),
#   Delimiter(" ",              (23,23)),
#   Set("Zealan",               (24,29)),
#       Word("Zealan",          (24,29)),   translated with custom pronuniation list
#   ),
#   Delimiter(".",              (30,30)),
# ]
# ----------------------------------------



#   Sentence("+1 801-520-3340 ADHD ASMR #123.422 21st! verycool $1,000.0,,,, 2% 2ndly?")
# ----------------------------------------
#   Set("+1 801-520-3340",      (0, 16)),       before
#   Set(" ADHD ASMR ",          (17,27)),
#   Set("#123.422",             (28,35)),       before
#   Set(" 21st! verycool ",     (36,50)),
#   Set("$1,000.0",             (51,59)),       before
#   Set(",,,, 2",               (60,65)),
#   Set("%",                    (66,66)),       before
#   Set(" 2ndly?",              (67,73)),
# ----------------------------------------


# ----------------------------------------
#   Set("+1 801-520-3340",      (0, 16)),
#   Set(" ADHD ASMR ",          (17,27)),
#       Delimiter(" ",              (17,17)),
#       Set("ADHD",                 (18,21)),
#           Word("A",                   (18,18), "eɪ"), ---pronounce with acronym pronouncer (pronounces Ay Bee See)
#           Delimiter(" "),
#           Word("D",                   (19,19), "di"),
#           Delimiter(" "),
#           Word("H",                   (20,20), "eɪʧ"),
#           Delimiter(" "),
#           Word("D",                   (21,21), "di"),
#       ),
#       Delimiter(" ",              (22,22)),
#       Set("ASMR",                 (23,26)),
#           Word("A",                   (23,23), "eɪ"), 
#           Delimiter(" "),
#           Word("S",                   (24,24), "ɛs"),
#           Delimiter(" "),
#           Word("M",                   (25,25), "ɛm"),
#           Delimiter(" "),
#           Word("R",                   (26,26), "ɑr"),
#       ),
#       Delimiter(" ",              (27,27)),
#   ),
#   Set("#",                    (28,28)),
#   Set("123.422",              (29,35)),   translated with num2words
#       Set("123",type="number"     (29,31)),
#           Word("one",                 (29,29)),
#           Delimiter(" "),
#           Word("hundred"),
#           Delimiter(" "),
#           Word("and"),
#           Delimiter(" "),
#           Word("twenty",              (30,30)),
#           Delimiter(" "),
#           Word("three",               (31,31)),
#       ),
#       Delimiter(" "),
#       Word(".",asif="point"    (32,32)),
#       Delimiter(" "),
#       Set("422",type="number"                         (33,35)),
#           Word("four",                (33,33)),
#           Delimiter(" "),
#           Word("two",                 (34,34)),
#           Delimiter(" "),
#           Word("two",                 (35,35)),
#       ),
#       Set("123",       (29,31)),
#   Set(" 21st! verycool ",       (36,50)),
#   Set("$1,000.0",               (51,59)),
#   Set(",,,, 2",                 (60,65)),
#   Set("%",                      (66,66)),
#   Set(" 2ndly?",                (67,73)),



# the default state of a delimiter is " "

#Sentence("    +1 801-520-3340 ADHD ASMR #123.422 21st! vérycool $1,022.0,,,, 2% 2ndly?")                               uses custom unidecode &&&& remove whitespace on ends
#   Set("+1 801-520-3340 ADHD ASMR #123.422 21st! verycool $1,022.0,,,, 2% 2ndly?", (0,73)){
# -     Set("+1 801-520-3340",                                                  (0,14),     type="phoneNumber"){        uses phoneNumber converter
#           Set("+",                                                                (0, 0),     type="symbol"){         uses symbol converter
#               Word("+",                                                               (0, 0),     asif="plus")
#           },
#           Delimiter(),
#           Set("1",        this part can be multiple numbers in a phone number     (1, 1),     type="indivNumbers"){   uses indivNumbers converter
#               Set("1",                                                                (1, 1)){                        uses num2words converter
#                   Word("1",                                                               (1, 1),     asif="one")    
#               }, 
#           },
# 
#  $1.05
#  one dollar, five cents
#  word1 word$ word5 wordcents
# 
#           Delimiter(" ",                                                          (2, 2),     asif=","),
#           Set("801",                                                              (3, 5),     type="indivNumbers"){   uses indivNumbers converter
#               Set("8",                                                                (3, 3)){                        uses num2words converter
#                   Word("8",                                                               (3, 3), asif="eight")
#               }, 
#               Delimiter(),
#               Set("0",                                                                (4, 4), asif=Word(asif="o",type="acronym")){ asif from phoneNumber converter - uses acronym converter
#                   Word("0",                                                               (4, 4), asif="zero")
#               }, 
#               Delimiter(),
#               Set("1",                                                                (5, 5)){                        uses num2words converter
#                   Word("1",                                                               (5, 5), asif="one")
#               }, 
#           },
#           Delimiter("-",                                                          (6, 6),     asif=Delimiter(",")),   asif from phoneNumber converter
#           Set("520",                                                              (7, 9),     type="indivNumbers"){   uses indivNumbers converter
#               Set("5",                                                                (7, 7)){                        uses num2words converter
#                   Word("5",                                                               (7, 7), asif="five")            asif from num2words converter
#               },
#               Delimiter(),
#               Set("2",                                                                (8, 8)){                        uses num2words converter
#                   Word("2",                                                               (8, 8), asif="two")             asif from num2words converter
#               }, 
#               Delimiter(),
#               Set("0",                                                                (9, 9)){                        uses num2words converter
#                   Word("0",                                                               (9, 9), asif="zero")            asif from num2words converter
#               }, 
#           },
#           Delimiter("-",                                                          (10,10),    asif=Delimiter(",")),   asif from phoneNumber converter
#           Set("3340",                                                             (11,14),    type="indivNumbers"){   uses indivNumbers converter
#               Set("3",                                                                (11,11)){                       uses num2words converter
#                   Word("3",                                                               (11,11), asif="three")
#               }, 
#               Delimiter(),
#               Set("3",                                                                (12,12)){                       uses num2words converter
#                   Word("3",                                                               (12,12), asif="three")
#               }, 
#               Delimiter(),
#               Set("4",                                                                (13,13)){                       uses num2words converter
#                   Word("4",                                                               (13,13), asif="four")
#               }, 
#               Delimiter(),
#               Set("0",                                                                (14,14)){                       uses num2words converter
#                   Word("0",                                                               (14,14), asif="zero")
#               }, 
#           },
#       },
#       Set(" ADHD ASMR #123.422 21st! verycool $1,022.0,,,, 2% 2ndly?",        (15,73)){
#           Set(" ADHD ASMR ",                                                      (15,25)){
#               Set(" ",                                                                (15,15)){
#                   Set(" ",                                                                (15,15)){                       uses delimiter converter
#                       Delimiter(" ",                                                          (15,15))
#                   },
#               },
# ---           Set("ADHD",                                                             (16,19),    type="acronym"){                uses acronym converter
#                   Word("A",                                                               (16,16)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("D",                                                               (17,17)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("H",                                                               (18,18)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("D",                                                               (19,19)     type="acronymletter")           uses acronym pronoucer
#               },
#               Set(" ASMR ",                                                           (20,25)){
#                   Set(" ",                                                                (20,20)){
#                       Set(" ",                                                                (20,20)){                                   uses delimiter converter
#                           Delimiter(" ",                                                          (20,20))
#                       },
#                   },
# ----              Set("ASMR",                                                             (21,24),    type="acronym"){                uses acronym converter
#                       Word("A",                                                               (21,21)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("S",                                                               (22,22)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("M",                                                               (23,23)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("R",                                                               (24,24)     type="acronymletter")           uses acronym pronoucer
#                   },
#                   Set(" ",                                                                (25,25)){
#                       Set(" ",                                                                (25,25)){                       uses delimiter converter
#                           Delimiter(" ",                                                          (25,25))
#                       },
#                   },
#               },
#           },
# --        Set("#"                                                                 (26,26),    type="hashtagNum"){     uses hashtag converter - types(hashtagWord, hashtagNum)
#               Word("number",                                                          (26,26))
#               Delimiter(),
#           },
#           Set("123.422 21st! verycool $1,022.0,,,, 2% 2ndly?",                    (27,73)){
#               Set("123.422 21st! verycool ",                                          (27,49)){
#                   Set("123.422 ",                                                         (27,34)){
# -----                 Set("123.422",                                                          (27,33),    type="number"){                   uses number converter
#                           Set("123",                                                              (27,29),    type="number"){
#                               
#                           },
#                           Word(".",asif="point"    (32,32)),
#                       },
#                       Set(" ",                                                                (34,34)){                       uses delimiter converter
#                           Delimiter(" ",                                                          (15,15))
#                       },
#                   },
# ----              Set("21st",                                                             (11,11)){
#                       
#                   },
#                   Set("! verycool ",                                                      (11,11)){
#                       
#                   },
#               },
# ---           Set("$1,022.0"                                                          (50,57),    type="currency"){   uses currency converter
#                   Set("1,022",                                                            (51,55),    type="number"){         uses number converter
#                       one thousand and twenty two
#                   },
#                   Delimiter(),
#                   Set("$",                                                                (50,50),    type="number"){         uses number converter
#                       
#                   },
#               },
#               Set(",,,, 2% 2ndly?",                    (34,73)){
#               },
#           },
#       },
#   }

#           Word(".",asif="point"    (32,32)),

#   Set("+1 801-520-3340",      (0, 16)),       before
#   Set(" ADHD ASMR #123.422 21st! verycool $1,000.0,,,, 2% 2ndly?",          (17,73)),
#   Set("#123.422",             (28,35)),       before
#   Set(" 21st! verycool ",     (36,50)),
#   Set("$1,000.0",             (51,59)),       before
#   Set(",,,, 2",               (60,65)),
#   Set("%",                    (66,66)),       before
#   Set(" 2ndly?",              (67,73)),
# ----------------------------------------

# testset = Set("    +1 801-520-3340 ADHD ASMR #123.422 21st! vérycool $1,022.0,,,, 2% 2ndly?", type="sentence")
# Set().tokenize
#>>>                                                               (0, 0),     asif="plus")
#           },
#           Delimiter(),
#           Set("1",        this part can be multiple numbers in a phone number     (1, 1),     type="indivNumbers"){   uses indivNumbers converter
#               Set("1",                                                                (1, 1)){                        uses num2words converter
#                   Word("1",                                                               (1, 1),     asif="one")    
#               }, 
#           },
# 
#  $1.05
#  one dollar, five cents
#  word1 word$ word5 wordcents
# 
#           Delimiter(" ",                                                          (2, 2),     asif=","),
#           Set("801",                                                              (3, 5),     type="indivNumbers"){   uses indivNumbers converter
#               Set("8",                                                                (3, 3)){                        uses num2words converter
#                   Word("8",                                                               (3, 3), asif="eight")
#               }, 
#               Delimiter(),
#               Set("0",                                                                (4, 4), asif=Word(asif="o",type="acronym")){ asif from phoneNumber converter - uses acronym converter
#                   Word("0",                                                               (4, 4), asif="zero")
#               }, 
#               Delimiter(),
#               Set("1",                                                                (5, 5)){                        uses num2words converter
#                   Word("1",                                                               (5, 5), asif="one")
#               }, 
#           },
#           Delimiter("-",                                                          (6, 6),     asif=Delimiter(",")),   asif from phoneNumber converter
#           Set("520",                                                              (7, 9),     type="indivNumbers"){   uses indivNumbers converter
#               Set("5",                                                                (7, 7)){                        uses num2words converter
#                   Word("5",                                                               (7, 7), asif="five")            asif from num2words converter
#               },
#               Delimiter(),
#               Set("2",                                                                (8, 8)){                        uses num2words converter
#                   Word("2",                                                               (8, 8), asif="two")             asif from num2words converter
#               }, 
#               Delimiter(),
#               Set("0",                                                                (9, 9)){                        uses num2words converter
#                   Word("0",                                                               (9, 9), asif="zero")            asif from num2words converter
#               }, 
#           },
#           Delimiter("-",                                                          (10,10),    asif=Delimiter(",")),   asif from phoneNumber converter
#           Set("3340",                                                             (11,14),    type="indivNumbers"){   uses indivNumbers converter
#               Set("3",                                                                (11,11)){                       uses num2words converter
#                   Word("3",                                                               (11,11), asif="three")
#               }, 
#               Delimiter(),
#               Set("3",                                                                (12,12)){                       uses num2words converter
#                   Word("3",                                                               (12,12), asif="three")
#               }, 
#               Delimiter(),
#               Set("4",                                                                (13,13)){                       uses num2words converter
#                   Word("4",                                                               (13,13), asif="four")
#               }, 
#               Delimiter(),
#               Set("0",                                                                (14,14)){                       uses num2words converter
#                   Word("0",                                                               (14,14), asif="zero")
#               }, 
#           },
#       },
#       Set(" ADHD ASMR #123.422 21st! verycool $1,022.0,,,, 2% 2ndly?",        (15,73)){
#           Set(" ADHD ASMR ",                                                      (15,25)){
#               Set(" ",                                                                (15,15)){
#                   Set(" ",                                                                (15,15)){                       uses delimiter converter
#                       Delimiter(" ",                                                          (15,15))
#                   },
#               },
# ---           Set("ADHD",                                                             (16,19),    type="acronym"){                uses acronym converter
#                   Word("A",                                                               (16,16)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("D",                                                               (17,17)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("H",                                                               (18,18)     type="acronymletter")           uses acronym pronoucer
#                   Delimiter(),
#                   Word("D",                                                               (19,19)     type="acronymletter")           uses acronym pronoucer
#               },
#               Set(" ASMR ",                                                           (20,25)){
#                   Set(" ",                                                                (20,20)){
#                       Set(" ",                                                                (20,20)){                                   uses delimiter converter
#                           Delimiter(" ",                                                          (20,20))
#                       },
#                   },
# ----              Set("ASMR",                                                             (21,24),    type="acronym"){                uses acronym converter
#                       Word("A",                                                               (21,21)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("S",                                                               (22,22)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("M",                                                               (23,23)     type="acronymletter")           uses acronym pronoucer
#                       Delimiter(),
#                       Word("R",                                                               (24,24)     type="acronymletter")           uses acronym pronoucer
#                   },
#                   Set(" ",                                                                (25,25)){
#                       Set(" ",                                                                (25,25)){                       uses delimiter converter
#                           Delimiter(" ",                                                          (25,25))
#                       },
#                   },
#               },
#           },
# --        Set("#"                                                                 (26,26),    type="hashtagNum"){     uses hashtag converter - types(hashtagWord, hashtagNum)
#               Word("number",                                                          (26,26))
#               Delimiter(),
#           },
#           Set("123.422 21st! verycool $1,022.0,,,, 2% 2ndly?",                    (27,73)){
#               Set("123.422 21st! verycool ",                                          (27,49)){
#                   Set("123.422 ",                                                         (27,34)){
# -----                 Set("123.422",                                                          (27,33),    type="number"){                   uses number converter
#                           Set("123",                                                              (27,29),    type="number"){
#                               
#                           },
#                           Word(".",asif="point"    (32,32)),
#                       },
#                       Set(" ",                                                                (34,34)){                       uses delimiter converter
#                           Delimiter(" ",                                                          (15,15))
#                       },
#                   },
# ----              Set("21st",                                                             (11,11)){
#                       
#                   },
#                   Set("! verycool ",                                                      (11,11)){
#                       
#                   },
#               },
# ---           Set("$1,022.0"                                                          (50,57),    type="currency"){   uses currency converter
#                   Set("1,022",                                                            (51,55),    type="number"){         uses number converter
#                       one thousand and twenty two
#                   },
#                   Delimiter(),
#                   Set("$",                                                                (50,50),    type="number"){         uses number converter
#                       
#                   },
#               },
#               Set(",,,, 2% 2ndly?",                    (34,73)){
#               },
#           },
#       },
#   }




# print(ipa.cmu_to_ipa("pee"))
# print(ipa.cmu_to_ipa("pm"))
# print(ipa.cmu_to_ipa("pee em"))
# print(ipa.convert("pee"))
# print(ipa.convert("pm"))
# print(ipa.convert("pee em"))
# print(ipa.convert("p m"))
# print(ipa.convert("johnny"))
# print(ipa.convert("aim"))
# print(ipa.convert("deep"))
# print(ipa.convert("a watermelon is read"))
# print(ipa.ipa_list("a"))
# print(ipa.ipa_list("s"))
# print(ipa.ipa_list("m"))
# print(ipa.ipa_list("t"))