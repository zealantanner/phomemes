import eng_to_ipa as ipa
import re
from replaceList import *

madetotest = "In sem justo, commodo ut, suscipit at???? pharetra vitae, orci. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Pellentesque habitant morbi tristique senectus et netus...? et malesuada fames ac turpis egestas.!!!? Aliquam id dolor!!!. Class aptent taciti sociosqu ad litora"

# use | to symbolize a nothing symbol

class Sentence:
    def __init__(self, data:list):
        self.data:list = data

        # if notsentence: raise Sentence.NotSentenceError(list)
        # self.isexclamation = 
    def __str__(self):
        pass
        # return "gobbledegook"
    # def (text):

        # return 
    class NotSentenceError(Exception):
        """Not a valid sentence"""
        def __init__(self, message):
            self.message = message
            super().__init__("\"" + message + f"\" is not a valid sentence")
        def __str__(self):
            return super().__str__()

class Token:
    def __init__(self, isword, isdelimiter):
        self.isword = isword
        self.isdelimiter = isdelimiter # is there a way to do this in token? look into that
    def remove_else(text:str):
        return re.sub(r"[^a-zA-Z\|\ ,\.\?!]","",text)
        # remove anything that isn't "a-zA-Z| ,.?!"
    def convert_to_list(text):
        # text = re.sub(r"[^0-9a-zA-Z" + re.escape("".join(Delimiter.pauseDelimiters)) + r"]", " ", text)
        # check if anything in any of the lists matches and if so return error
        return text
    
# isalreadyIPA:bool=False

class Delimiter(Token):
    exclamation = "!"
    question = "?"
    period,wannabePeriod = ".","\n\f\t\v"
    comma,wannabeComma = ",","~—():;"
    space,wannabeSpace = " ","-_/\\"
    blank = "|"
    allDelimiters = exclamation + question + period + wannabePeriod + comma + wannabeComma + space + wannabeSpace + blank
    def __init__(self, type:str="."):
        self.type = type
        self.is_space:bool = False
        self.is_comma:bool = False
        self.is_period:bool = False
        self.is_question:bool = False
        self.is_exclamation:bool = False
        super().__init__(False, True)
        match type:
            case " ": self.is_space = True
            case ",": self.is_comma = True
            case ".": self.is_period = True
                # case "?": self.is_question = True
                # case "!": self.is_exclamation = True

    # exclamationDelimiters = ("!")
    # questionDelimiters = ("?")
    # periodDelimiters = (".","!","?","\n","\f","\t","\v")
    # commaDelimiters = (",","~","—","(",")",":",";")
    # spaceDelimiters = (" ","-","_","/","\\")
    # blankDelimiters = ("|")
    # allDelimiters = exclamationDelimiters + questionDelimiters + periodDelimiters + commaDelimiters + spaceDelimiters + blankDelimiters

    # def delimit(self, others):
    #     print("~1",self.chars)
    #     print("~2",others)
    #     return r"[" + self.reg + Delimiter(others).reg + r"]*[" + self.reg + r"*]+[" + self.reg + Delimiter(others).reg + r"]*"
    # def identify_delimiters(text:str):
    #     return text
    def condense_delimiters(text:str):
        def wannabe_remover(text:str):
            print("start wannabe remove")
            newt = text
            newt = re.sub(r"([" + re.escape(Delimiter.wannabePeriod) + r"])\1+",".",newt)
            newt = re.sub(r"([" + re.escape(Delimiter.wannabeComma) + r"])\1+",",",newt)
            newt = re.sub(r"([" + re.escape(Delimiter.wannabeSpace) + r"])\1+"," ",newt)
            return newt
        def dupe_remover(text:str): # 1:32 3:00 am 12:63
            print("start dupe remove")
            newt = text
            print(text)
            search = re.search((r"([" + Delimiter.allDelimiters + r"])\1+"),newt)
            if(search):
                newt = re.sub(re.escape(search.group()),search.group(1),newt)
                newt = dupe_remover(newt)
            return newt
        def lower_remover(text:str):

            lowRemove = Pattern("separate delimiters",
                r"(?:(\|)|(\ )|(,)|(\.)|(!)|(\?))+",
                # 1:"|" 2:" " 3:"," 4:"." 5:"!" 6:"?"
            lambda r,t: re.search(r,t))
            
            delimiterList = lowRemove.findall(text)
            print(delimiterList)
            return text
        print("lower_remover")
        print(lower_remover(";aslkdjfalks alksjd flkja sl lkajs dfj sldk a? ,,,,,,,,,,,,,,,.,| asfa"))


        # periodDelimiters = rf"[\ \,\.]*[\.*]+[\ \,\.]*"
        # exclamationDelimiters = ["!"]
        # questionDelimiters = [""]
        
        # periodDelimiters1 = Delimiter(periodPauseDelimiters)
        # print(1,periodDelimiters1.delimit(space + comma))
        # periodDelimiters2 = r"[" + space + comma + period + r"]*[" + period + r"*]+[" + space + comma + period + r"]*"
        # print(2,periodDelimiters2)
        # commaDelimiters = r"[" + space + comma + r"]*[" + comma + r"*]+[" + space + comma + r"]*"
        # spaceDelimiters = r"[" + space + r"]*[" + space + r"*]+[" + space + r"]*"

        # exclamaitionDelimiters
        # questionDelimiters
        # exclamation

        # text = re.sub(periodDelimiters, ".", text)
        # text = re.sub(commaDelimiters, ",", text)
        # text = re.sub(spaceDelimiters, " ", text)
        # print(periodPauseDelimiters)
        # print(periodDelimiters)
        # print(text)
        text = text+"."
        text = wannabe_remover(text)
        text = dupe_remover(text)
        text = lower_remover(text)
        return text
    


class Word(Token):
    def __init__(self, text): # emphasis=False
        super().__init__(True, False)

    def to_IPA(word):
        pass
    class InvalidWord(Exception):
        """Not a valid word"""


print(Delimiter.condense_delimiters("asdlfkjal.............--------....skdjfl  ..??asfd123123::;;?!!alskjdhflk"))

# Delimiter.condense_delimiters(madetotest)

# print(Word)
# print(p.apply_punct(["hello",",,,,  .... ","sweet"," cheeks. what's up bbryu."], True))
# print(p.fetch_words("hello"))
# print(p.fetch_words("asdfas"))
# print(p.cmu_to_ipa(p.get_cmu("hello")))
# print(p.get_top("321"))
# print(Sentence([123]))
print(ipa.ipa_list("dont"))
print(ipa.ipa_list("gonna"))
print(ipa.ipa_list("boyfriend"))
print(ipa.ipa_list("boyfriend"))
