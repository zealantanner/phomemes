import eng_to_ipa as p 
import re
from constants import *

# periodPauseDelimiters = ".!&?\n"
# commaPauseDelimiters  = ",~*()=+\\:;\""
# spacePauseDelimiters  = " -_></"


delimiters = periodPauseDelimiters+commaPauseDelimiters+spacePauseDelimiters
# print(delimiters)
# print(delimiters[4],delimiters[12])
def split(string:str, delimiters=delimiters, maxsplit=0):
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])
    





# def replace_delimiters1(token:str):
#     period= re.escape(periodPauseDelimiters)
#     comma = re.escape(commaPauseDelimiters)
#     space = re.escape(spacePauseDelimiters)
    
#     periodDelimiters = r"[^" + period + "]*[" + period + "]+[^" + period + "]*"
#     commaDelimiters  = r"[^" + comma  + "]*[" + comma  + "]+[^" + comma  + "]*"
#     spaceDelimiters  = r"[^" + space  + "]*[" + space  + "]+[^" + space  + "]*"
    
#     # token = token.lstrip(re.escape(delimiters))
#     token = re.sub(periodDelimiters,".",token)
#     token = re.sub(commaDelimiters,",",token)
#     token = re.sub(spaceDelimiters," ",token)
#     return token

def condense_delimiters(text:str):
    period = re.escape("".join(periodPauseDelimiters))
    comma = re.escape("".join(commaPauseDelimiters))
    space = re.escape("".join(spacePauseDelimiters))
    # periodDelimiters = rf"[\!\?\.\?\‽\n*]+"
    # periodDelimiters = rf"[\ \,\.]*[\.*]+[\ \,\.]*"
    periodDelimiters = r"[" + space + comma + period + r"]*[" + period + r"*]+[" + space + comma + period + r"]*"
    commaDelimiters = r"[" + space + comma + r"]*[" + comma + r"*]+[" + space + comma + r"]*"
    spaceDelimiters = r"[" + space + r"]*[" + space + r"*]+[" + space + r"]*"


    text = re.sub(periodDelimiters, ".", text)
    text = re.sub(commaDelimiters, ",", text)
    text = re.sub(spaceDelimiters, " ", text)
    # print(periodPauseDelimiters)
    # print(periodDelimiters)
    # print(text)
    return text

# print(condense_delimiters("the?.re  .,,   .  wa,     ,,,    ,s a ???????.?????\\|(so-called) ro"))


def replace_delimiters(text:str):
    text = text.lstrip(re.escape(delimiters))
    return [condense_delimiters(token) for token in re.split(r"\b",text) if token!=""]
# apply

def replace_times(text:str):
    for x in replaceTime:
        if(re.search(x[0],text)):
            # print(re.sub(x[0], x[1](text), text))
            text = re.sub(x[0], x[1](text), text)
            replace_times(text)
        else:
            return text



def convert_nums_to_words(text:str):
    newtext = ""
    for x in re.findall(r"[0-9]+|[^0-9]+",text):
        if(re.search(r"[0-9]+", x)):
            print(num2words(x))
            newtext = "".join([newtext, " ", num2words(x), ""])
        else:
            print(x)
            newtext = "".join([newtext, x])
    return newtext

def replace_unknowns(text:str): 
    for x in unknownDict:
        if(re.search(x, text)):
            text = re.sub(x, unknownDict[x],text)
        replace_unknowns(text)
    return text


def unconfuse(text:str):
    text = replace_times(text)
    text = replace_unknowns(text)
    text = convert_nums_to_words(text)
    return text
    
# order is: specialgroupdict, unknownDict, numbers to words, Delimiter



def is_delimiter(text:str):
    return any(elem in text for elem in delimiters)

def is_word(s):
    return (p.isin_cmu(s) and len(s)>0 and not is_delimiter(s))




testtext = [
    "electriccompany",
    "begladyournoseisonyourface",
    "Once 1:20 pm @ #sussyland appleb 12:00 am ananacherroy there 12:04 Pm     was a ????????????\\|(so-called) rock. it.,was not! in fact, a big rock.",
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






print(unconfuse(testtext[2]))




