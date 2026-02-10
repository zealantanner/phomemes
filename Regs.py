import re
from mess import Pattern, SetNode, Sentence, Token, Word, Delimiter
from num2words import num2words as n2w
from Qualities import colors, say_span
from __future__ import annotations
import delimit
#> make sure unidecode doesn't change ¿¡‘’“”£¢∞π§œ∑´®†¥¨ˆøπ“‘åß∂ƒ©˙∆˚¬…æ≈ç√∫˜µ≤≥÷
# blankDelimiters = ("|") #> dont do this

groupize_neutralSingleQuote = Pattern(re.compile( # specifically for '' # considers "won't" and "lucas'"
    r"""(?P<selection1> #> make it case insensitive
            (?P<first1>
                (?<![a-z0-9'])'(?!(?:bout|cause|cept|em|neath|til|tis|twas|tween|twere)[^a-z])
            )
            (?P<content1>.*?)
            (?<!s)(?P<second1> 
                (?<![^a-z0-9](?:ol))'(?![a-z0-9'])
            )
        )
        |
        (?P<selection2>
            (?P<first2>
                (?<![a-z0-9'])'(?!(?:bout|cause|cept|em|neath|til|tis|twas|tween|twere)[^a-z])
            )
            (?P<content2>.*?)
            (?P<second2>
                (?<![^a-z0-9](?:ol))'(?![a-z0-9'])
            )
        )
    """, flags=re.X|re.I),
    lambda span, m: groupize_neutralSingleQuote(span, m),
    "'single neutral quotation marks'")
groupize_neutral = 1
groupize = [groupize_neutralSingleQuote, groupize_neutraldoubleQuote]
def groupize_func(span, m):
    #> 
    pass

def num2words_func(span, m):
    # Pattern(re.compile(r"\w+-\w+"), lambda span, m: "dashes between", type="text")
    # repl = n2w(m)
    # search = re.search(reg, text)
    return SetNode(span,m,)
num2words = Pattern(re.compile(
    r"""(?P<isminus>-)?
        (?P<number>
            (?P<justdecimal>
                (?P<justdecpoint>\.)
                (?P<justdecdigits>\d+)
            )
        |
            (?P<integer>
                (?P<withcommas>
                    (?:\d{1,3})
                    (?:,\d{3})+
                )
            |
                (?P<nocommas>\d+)
            )
            (?P<decimal>
                (?P<decpoint>\.)
                (?P<decdigits>\d+)
            )?
        )
    """, flags=re.VERBOSE),
    lambda span, m: num2words_func(span, m),
    desc="num2words")
    

def wordspaceword_func(span, m):

    return SetNode(span, m)
wordspaceword = Pattern(re.compile(
    #> may not work with delimiter variables, figure that out
    r"""(?<=\w)
        (?P<selection>[\ \-,\.\?\!]+) #> use delimiter variables
        (?=\w) #
    """, flags=re.VERBOSE),
    lambda span, m: wordspaceword_func(span, m),
    desc="wordspaceword")

def delimitize_func(span, m):
    return SetNode(span,m)
delimitize = Pattern(re.compile(
    r"""
        (?P<selection>[\ \-,\.\?\!]+)
    """, flags=re.VERBOSE),
    lambda span, m: delimitize_func(span, m),
    desc="delimitize")



#> functionality for math symbols, call each of symbols what they are 
#> like "is greater than or equal to" if there's numbers being compared ≤≥÷+-
rules = [
    # maybe??? if I want to specify if something should be bold or italic, go with <i>hello</i>. use html style
    # groupize, # --unfinished like ¡hi! or "what" or but not for "didn't he's brooks' "
    # trailingDelimiter, # "hi " "hi," "hi." --unfinished
    # symbols, # like π or ∞ --unfinished
    # fractionSymbols, # ½ --unfinished
    # degrees, # ° --unfinished
    # currency, # --unfinished
    # time, # clock time # --unfinished
    # url_or_email, # --unfinished
    # phoneNumbers, # --unfinished
    # hashtag, # # # --unfinished
    # apostrophewords
    # abbreviations, # l84 b4 i.e. e.g. misc. etc. --unfinished
    # fileExtensions, # --unfinished
    # ordinal numbers, # (including 2ndly) --unfinished
    # fractions, # 1/2 2/3 --unfinished
    num2words, # with type indivNumbers, add e notation --unfinished
    wordspaceword, # --unfinished
    delimitize, # --unfinished
    # wordize, # with type acronym, --unfinished
]



start_rules = [
    # multisentencesplitter, # for \n --unfinished
    # customUnidecode, # that doesn't touch symbols like ¢ £ π ∞ ½ --unfinished
]


