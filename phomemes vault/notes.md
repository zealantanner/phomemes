input text

how does it pronounce "mr" and "mrs" with eng_to_ipa

when a token has a subspan, that means it should be the final in some cases.
write functions for getting all the leaf children, as well as all the lowest ones without subspans. that way they can be grouped correctly in some cases.
"I want $100"
"(I)( )(want)( )($100)"




possessive:
it's just an 's, unless the subject ends in s, then it can just be '
for example:
david's
james'
james's
Use the regex I made for detecting the apostrophe vs quotation marks
'I go to jonas' house'


give groups of text the option of being bold or italic with parameters



Try my program with different books with text.


Make it so it can detect characters by the names in bits of text


for cases like $100.01 it should be one hundred dollars and 1 cent
with that .01 being singular

$ could go at the end too . "I have 100$"


add all the info inheritance after adding basic functions

use spellchecker

I have ∞ dollars

Nooooooooooooooooooo
No + ox10+ o


1098274j098d079n1809812n3098d1y20n398dh10

REGEX


Have a thing for finding patterns, and another for converting.
When a pattern is matched, it activates the convertby function


Can I have $100 of Jonas' 1st paycheck? Thnak you
Can I have one hundred dollars of Jonas' first paycheck? Thank you


1stly
firstly
12:10 pm


group things into groups like "" and () after already tokenizing

For acronyms:
Each letter should correspond to each word

initialism vs acronym

for acronyms like API, make sure to use the phonemer but make sure it's the letters, a can sound like uh if it's the word.
just have a parameter for 







Word((0,3),"Can"),
Delimiter((3,4)," "),
Word((4,5),"I"),
Delimiter((5,6)," "),
Word((6,10),"have"),
Delimiter((10,11)," "),
Word((12,15,(0,3)),"one"),
Delimiter((12,15,(3,4))," "),
Word((12,15,(4,11)),"hundred"),
Delimiter((12,12)," "),
Word((11,12,(0,7)),"dollars",info={currency:True,currency.dollar:True,plural:True}),
Delimiter((15,16)," "),
Word((16,18),"of"),
Delimiter((18,19)," "),
Name((19,25),"Jonas'",info={span:(19,24),text:"Jonas",},possessive=True,possessiveInfo={span:(24,25),text:"'"}),
Delimiter((25,26)," "),
Word((26,29,(0,5)),"first"),
Delimiter((29,30)," "),
Word((30,38),"paycheck"),
Delimiter((38,39),"?",type={question:True,sentenceEnd:True}),
Delimiter((39,40)," "),
Word((40,45,(0,5)),"Thank"),
Delimiter((45,46)," "),
Word((46,49),"you"),

















future:
detect nouns and subjects,