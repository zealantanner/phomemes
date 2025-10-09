import re
from mess import Pattern, SetNode, Sentence, Token, Word, Delimiter
from num2words import num2words as n2w
from Qualities import colors, say_span
from __future__ import annotations



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
    """, flags=re.X),
    lambda span, m: num2words_func(span, m),
    "num2words")
    

def wordspaceword_func(span, m):
    return SetNode(span, m)
wordspaceword = Pattern(re.compile(
    r"""(?P<start>\w+)
        (?P<selection>\ )
        (?P<end>\w.+)
    """
),)

rules = [
    # trailingDelimiter "hi " "hi," "hi."
    # symbols, # like π or ∞
    # fractionSymbols, # ½
    # degrees, # °
    # currency,
    # time, # clock time
    # url_or_email,
    # phoneNumbers,
    # hashtag, # # #
    # abbreviations, # l84 b4 i.e. e.g. misc. etc.
    # fileExtensions,
    # ordinal numbers, (including 2ndly)
    # fractions, # 1/2 2/3
    num2words, # with type indivNumbers
    wordspaceword,
    # delimitize,
    # wordize, with type acronym
]



start_rules = [
    # custom unidecode that doesn't touch symbols like ¢ £ π ∞ ½
]