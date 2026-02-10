


Names:
delimiter: "the" {the} (the) ¿the?


order of operations:



- classify
    - invalid_character
        once this is used it doesn't need to run ever again.

    - trailing_joiner
        - start
            " hello"
        - end
            "hello "

    - enclosure
        include edge case for possible 
        - symmetric_pairs
            - parentheses
                (...)
            - brackets
                [...]
            - curly_brackets
                {...}
            - angle_brackets
                ⟨...⟩
            - less_than_greater_than
                <...>
        - quotation
            - double
                "...",“...”,«...»
            - single
                '...',‘...’,‹...›
        - inverted_punctuation
            - question
                ¿...?
            - exclamation
                ¡...!
        - emphasis
            - asterisk
                *...*,**...**,***...***
            - _..._
            - ~...~
            - ^...^
        - code
            `...`,```...```
    - email_or_url
        thing@thing.thing
    - time
        12:04 pm
    - currency
        - dollars
            - cents
        - pounds
            - pence
        - euros
            - cents
        - yen
    - degrees
        just degrees would just mean °
        - F
            °F
        - C
            °C
        - K
            °K
    - phone_number
    - hashtag
        #cool
        - number
            #12
    - number
        - ordinal_number
            1st 2nd 3rd 4th
            - plural
                1sts 3rds 5ths
            - ly
                3rdly
            - nth????????
        - fraction
        - integer
            check for commas
        - decimal

    - abbreviations
        "i.e.", "e.g.", "misc.", "etc."
    - word_joiner_word
        "hello there"
    - word_like
        - names
        - acronym
        - word
    <!-- - delimiter -->



- transform
    - currency
        - dollars
            $12.34
            - cents
                .34
        - euros
            - cents
        - pounds
            - pence
        - yen
    - number
        - commas
            1,234
        - decimal
            .1234
        - fraction
            12/34
        - integer
            1234
        - ordinal
            1234th (can have commas)
            - ly
                1stly
            - plural
                2nds
    - word_like
        - acronym

        - names
            zealan


fat4the
1o7n3ltnf87ej48r


this (is a "cool) sentence" I think"

this (is a "cool) sentence" I think"


- Set((0,36,36),`this (is a "cool) sentence"I think"`)
  - Set()
  - Enclosure()



define sentences afterward, don't make them into sets



Functions that need to be made
transform
[
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



space	Whitespace
tab/newline	Whitespace
comma	Separator
period	Terminator
question mark	Terminator
exclamation	Terminator
dash    Joiner
slash   Joiner
apostrophe	Modifier
brackets	Enclosure




He whispered ("very quietly.").
                  end is here ^