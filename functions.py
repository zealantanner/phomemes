import eng_to_ipa as p 
import re
from replaceList import *

# periodPauseDelimiters = ".!&?\n"
# commaPauseDelimiters  = ",~*()=+\\:;\""
# spacePauseDelimiters  = " -_></"

class Delimiter:
    def __init__(self, chars):
        self.chars = chars
        self.string = "".join(chars)
        self.reg = re.escape(self.string)
    
    def delimit(self, others):
        print("~1",self.chars)
        print("~2",others)
        return r"[" + self.reg + Delimiter(others).reg + r"]*[" + self.reg + r"*]+[" + self.reg + Delimiter(others).reg + r"]*"

    def sub(self, repl, string ,count: int = 0):
        return re.sub(self.reg, repl, string, count)
    # def __str__()

class Pause:
    def __init__(self, type:str="."):
        self.type = type
        self.is_space:bool = False
        self.is_comma:bool = False
        self.is_period:bool = False
        self.is_question:bool = False
        self.is_exclamation:bool = False
        match type:
            case " ": self.is_space = True
            case ",": self.is_comma = True
            case ".": self.is_period = True
            case "?": self.is_question = True
            case "!": self.is_exclamation = True
        pass
    def __str__(self):
        return self

    

delimiters = periodPauseDelimiters+commaPauseDelimiters+spacePauseDelimiters

# def split(string:str, delimiters=pauseDelimiters, maxsplit=0):
#     regex_pattern = '|'.join(map(re.escape, delimiters))
#     return re.split(regex_pattern, string, maxsplit)

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def condense_delimiters(text:str):
    period = re.escape("".join(periodPauseDelimiters))
    comma = re.escape("".join(commaPauseDelimiters))
    space = re.escape("".join(spacePauseDelimiters))
    # periodDelimiters = rf"[\ \,\.]*[\.*]+[\ \,\.]*"
    # exclamationDelimiters = 
    # questionDelimiters =
    periodDelimiters1 = Delimiter(periodPauseDelimiters)
    print(1,periodDelimiters1.delimit(space + comma))
    periodDelimiters2 = r"[" + space + comma + period + r"]*[" + period + r"*]+[" + space + comma + period + r"]*"
    print(2,periodDelimiters2)
    # commaDelimiters = r"[" + space + comma + r"]*[" + comma + r"*]+[" + space + comma + r"]*"
    # spaceDelimiters = r"[" + space + r"]*[" + space + r"*]+[" + space + r"]*"


    # text = re.sub(periodDelimiters, ".", text)
    # text = re.sub(commaDelimiters, ",", text)
    # text = re.sub(spaceDelimiters, " ", text)
    # print(periodPauseDelimiters)
    # print(periodDelimiters)
    # print(text)
    return text

# print(condense_delimiters("the?.re  .,,   .  wa,     ,,,    ,s a ???????.?????\\|(so-called) ro"))

# print(condense_delimiters("the?.re  .,,   .  wa,     ,,,    ,s a ???????.?????\\|(so-called) ro"))


# def replace_delimiters(text:str):
#     text = text.lstrip(re.escape(delimiters))
#     return [condense_delimiters(token) for token in re.split(r"\b",text) if token!=""]
# apply



def replace_unknowns(text:str):
    for unknownSymbol in unknownDict:
        search = re.search(re.escape(unknownSymbol), text)
        if(search):
            text = re.sub(search.group(), unknownDict[unknownSymbol], text)
            text = replace_unknowns(text)
    return text

def replace_specials(text:str):
    for special in specialGroupDict:
        search = re.search(re.escape(special), text)
        if(search):
            text = re.sub(search.group(), specialGroupDict[special], text)
            text = replace_specials(text)
    return text


def replace_patterns(text:str):
    # loop over every pattern in order
    for pattern in replacePatterns:
        search = re.search(pattern[0],text)
        if(search):
            print(f"replaced \"{search.group()}\" with \"{pattern[1](text)}\"")
            text = re.sub(pattern[0], pattern[1](text), text)
            print(text)
            text = replace_patterns(text)
    return text


def convert_nums_to_words(text:str):
    newtext = ""
    for x in re.findall(r"[0-9]+|[^0-9]+",text):
        if(re.search(r"[0-9]+", x)):
            # print(num2words(x))
            newtext = "".join([newtext, " ", num2words(x), ""])
        else:
            # print(x)
            newtext = "".join([newtext, x])
    return newtext




def replace_delimiters(text:str):
    text = text.strip("".join(delimiters))
    text = condense_delimiters(text)
    return re.split(r"( |,|\.)", text)
    # return [condense_delimiters(token) for token in re.split(r"\b",text) if token!=""]


def remove_etc(text:str):
    text = re.sub(r"[^0-9a-zA-Z" + re.escape("".join(pauseDelimiters)) + r"]", " ", text)
    # check if anything in any of the lists matches and if so return error
    return text


# print(replace_delimiters("asdf.asdf,fdsa asdfd"))



# print(replace_unknowns("zealan@gmail@.com"))

def unconfuse(text:str):
    order_to_run = [
        replace_unknowns,
        replace_specials,
        replace_patterns,
        # convert_nums_to_words,
        # remove_etc,
        # condense_delimiters,
        # replace_delimiters,
        ]
    for function in order_to_run:
        # print(f"{function(text)=}")
        print(f"{function.__code__.co_name}(text)=\t{function(text)}")

        text = function(text)
    return text
    
# order is: specialgroupdict, unknownDict, numbers to words, Delimiter
temp = "1-1-100.23 12:30     am12:00 2:03pm misc."
print(temp)
print(unconfuse(temp))



def is_delimiter(text:str):
    return any(elem in text for elem in delimiters)

def is_word(s):
    return (p.isin_cmu(s) and len(s)>0 and not is_delimiter(s))




testtext = [
    "electriccompany",
    "begladyournoseisonyourface",
    "Once. 1:20 pm @ #sussyland appleb 12:00 am ananacherroy there 12:04 Pm     was a ????????????\\|(so-called) rock. it.,was not! in fact, a big rock.",
    "applebananacherry",
    "applesorangesandbananas",
    "appleorangebanana",
    "a",
    "abe",
    "Iaskedasimilar questionhereand theanswergiven doesuseany importsorcomprehensions Itdoeshave aforloop thoughAnyparticularly reasonforthatrequirement",
    "neighbourhood vs neighborhood In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam id dolor. Class aptent taciti sociosqu ad litora",
    "ThatsoneofthetopresultswhenIlookupwiitank",
    "applebeesgrillandbarmenu",
    "come @ me b1ro #gamer 100% m&m gimme a yummy ^",
    "go to #gamer@beans.com to win ä bïg tree... if not, that's ok"
]

# l=re.split(r"\b",testtext)
# print([replaceDelimiters(token) for token in re.split(r"\b",testtext) if token!=""])


# testtext = "The world is a       vampoire, and I love gobbbobagabboh"
# print(split("hello$there.mr Bubbles.it's{always^been!a)pleasure"))
# print(split("a b~c`d!e@f#g$h%i^j&k*l(m)n-o_p=q+r|s\\t}u]v{w[x:y;z\"A?B/C>D.E<F,G"))
# print(delimiters)
# shenaniganery


def cut_string_in_half(string):
    return [string[:len(string)//2], string[len(string)//2:]]
    

def zigzag_check(string):
    length = len(string)
    mid = length // 2
    offsets = [0]

    for i in range(1, mid + 1):
        offsets.append(i)
        offsets.append(-i)

    offsets = sorted(set(offsets), key=abs)
    results = []

    for offset in offsets:
        left = string[:mid + offset]
        right = string[mid + offset:]
        print(f"Checking: {left}|{right}")
        if is_word(left):
            results.append(left)
            print(f"Valid word: \"{left}\"")
            if is_word(right):
                results.append(right)
                print(f"Valid word: \"{right}\"")
                break
            else:
                results.append(zigzag_check(right))
            break
    return flatten(results)


def back_to_front_check(string):
    length = len(string)
    offsets = [0]

    for i in range(1, length):
        offsets.insert(0,i)

    results = []

    for offset in offsets:
        left = string[:offset]
        right = string[offset:]
        print(f"Checking: {left}|{right}")
        if is_word(left):
            results.append(left)
            print(f"Valid word: \"{left}\"")
            if is_word(right):
                results.append(right)
                print(f"Valid word: \"{right}\"")
                break
            else:
                results.append(back_to_front_check(right))
            break
    return flatten(results)


def front_to_back_check(string):
    length = len(string)
    offsets = [0]

    for i in range(1, length):
        offsets.append(i)

    results = []

    for offset in offsets:
        left = string[:offset]
        right = string[offset:]
        print(f"Checking: {left}|{right}")
        if is_word(right):
            results.insert(0,right)
            print(f"Valid word: \"{right}\"")
            if is_word(left):
                results.insert(0,left)
                print(f"Valid word: \"{left}\"")
                break
            else:
                results.insert(0,front_to_back_check(left))
            break
    return flatten(results)

def hopeless_check(string):
    results = [ch for ch in string]
    return flatten(results)




# def fix_broken_word(word:str):
#     array = []
#     # text = split(text)
#     if(not p.isin_cmu(word)):
#         for
#         word[:len(word)//2], word[len(word)//2:]

#     # for i in text:
#         # print(i)
#         if(p.isin_cmu(text)):
#             # s = cut_string_in_half(i[0])
#             # print(s)
#             # print("hello there buddy")


#         # if('*' in i[0]):
#             print("this word doesn't parse")

#         # print(first_half)
#         # print(second_half)
#         # print(i)
#     return []



def convert_to_pronounceable(text:str, method:int = 0):
    t = text
    t = replace_delimiters(t)

    match method:
        case 1:
            check = zigzag_check
        case 2:
            check = back_to_front_check
        case 3:
            check = front_to_back_check
        case 4:
            check = hopeless_check
        case _:
            check = back_to_front_check

    newText = []
    for word in t:
        if(is_delimiter(word) or is_word(word)):
            newText.append(word)
        else:
            newText.append(check(word))
    print(text)
    return flatten(newText)


# print(testtext)
# print(special_split(testtext))
# print('|'.join(map(re.escape, delimiters)))
# text3 = "yo ur cant"

# print([replaceDelimiters(token) for token in re.split(r"\b",text3)])
# print(replaceDelimiters(text3))
# for the in replaceDelimiters(text3):
#     if(not isDelimiter(the)):
#         print(the, " = ", p.isin_cmu(the))
# print(["asdf", cut_string_in_half("text3")])
# print(zigzag_split_and_check(testtext[8]))
# print(convert_to_pronounceable(testtext[8]))
# print(replaceDelimiters(text3))
# print(p.isin_cmu(text3))
# print(p.ipa_list(text3))
# print(convert_to_pronounceable(input("Enter some text: ")))






# print(unconfuse(testtext[2]))




