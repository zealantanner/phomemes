import eng_to_ipa as p 
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
    def convert(text):
        return "a"
    class NotSentenceError(Exception):
        """Not a valid sentence"""
        def __init__(self, message):
            self.message = message
            super().__init__(f"")
        def __str__(self):
            return super().__str__()

class Token:
    
    def remove_else(text:str):
        # text = re.sub(r"[^0-9a-zA-Z" + re.escape("".join(Delimiter.pauseDelimiters)) + r"]", " ", text)
        # check if anything in any of the lists matches and if so return error
        return text
    
# isalreadyIPA:bool=False

class Delimiter(Token):
    # exclamationDelimiters = ("!")
    # questionDelimiters = ("?")
    # periodDelimiters = (".","!","?","\n","\f","\t","\v")
    # commaDelimiters = (",","~","—","(",")",":",";")
    # spaceDelimiters = (" ","-","_","/","\\")
    # blankDelimiters = ("|")
    # allDelimiters = exclamationDelimiters + questionDelimiters + periodDelimiters + commaDelimiters + spaceDelimiters + blankDelimiters

    isword,isdelimiter = False,True
    def __init__(self):
        super().__init__(str)
    # def delimit(self, others):
    #     print("~1",self.chars)
    #     print("~2",others)
    #     return r"[" + self.reg + Delimiter(others).reg + r"]*[" + self.reg + r"*]+[" + self.reg + Delimiter(others).reg + r"]*"

    def condense_delimiters(text:str):
        exclamation = "!"
        question = "?"
        period = "".join([".","\n","\f","\t","\v"])
        comma = "".join([",","~","—","(",")",":",";"])
        space = "".join([" ","-","_","/","\\"])
        blank = "|"
        allDelimiters = exclamation,question,period,comma,space,blank
        # allDelimiters = r"([" + space + comma + period + exclamation + question + r"]*[" + period + exclamation + question + r"*]+[" + space + comma + period + exclamation + question + r"]*)+"
        # [x for x in range(10)]
        print(allDelimiters[:3])
        print(re.search(r"([" + "".join(allDelimiters) + r"]*[" + "".join(allDelimiters[:3]) + r"]+[" + "".join(allDelimiters) + r"]*)+",text))
        # text.partition
        # text = re.sub(exclamation, "!", text)
        # text = re.sub(question, "?", text)
        # text = re.sub(period, ".", text)
        # text = re.sub(comma, ",", text)
        # text = re.sub(space, " ", text)
        # text = re.sub(blank, "|", text)
        pattern = re.escape(r"([" + "".join(allDelimiters) + r"]*[" + "".join(allDelimiters[:3]) + r"]+[" + "".join(allDelimiters) + r"]*)+")
        search = re.search(pattern,text)
        if(search): # . ? !
            print(text)
            print(re.sub(pattern,"lemon",text))

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
        return text

class Word(Token):
    isword,isdelimiter = True,False
    def __init__(self, text, emphasis=False):pass
    def to_IPA(word):
        pass
    class InvalidWord(Exception):
        """Not a valid word"""


Delimiter.condense_delimiters(madetotest)

# print(Word)
# print(p.apply_punct(["hello",",,,,  .... ","sweet"," cheeks. what's up bbryu."], True))
# print(p.fetch_words("hello"))
# print(p.fetch_words("asdfas"))
# print(p.cmu_to_ipa(p.get_cmu("hello")))
# print(p.get_top("321"))
# print(Sentence([123]))