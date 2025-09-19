# import eng_to_ipa as ipa
# import re
# from newreplaceList import *
import unicodedata



texting = {
    1: "electriccompany",
    2: "begladyournoseisonyourface",
    3: "$100 $12.34 $1 $1.01 Once. 1:20 pm @ #sussyland #12 #12:03 appleb 12:00 am.com 1st 10th etc. ananacherroy there 12:04 Pm     was a ????????????\\|(so-called) rock. it.,was not! in fact, a big rock.",
    4: "applebananacherry",
    5: "applesorangesandbananas",
    6: "appleorangebanana",
    7: "a",
    8: "abe",
    9: "Iaskedasimilar questionhereand theanswergiven doesuseany importsorcomprehensions Itdoeshave aforloop thoughAnyparticularly reasonforthatrequirement",
    10: "neighbourhood vs neighborhood In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam id dolor. Class aptent taciti sociosqu ad litora",
    11: "ThatsoneofthetopresultswhenIlookupwiitank",
    12: "applebeesgrillandbarmenu",
    13: "come @ me b1ro #gamer 100% m&m gimme a yummy ^",
    14: "go to #gamer@beans.com to win ä bïg tree... if not, that's ok",
    15: "1:00 1-1-100.23 12:30     am12:00 2:03pm misc.",
    16: "win ä bïg tree #qwer check |||| #123.422 12:00 am 1st 11th 11,333,444,555.3 @ 21st 3rd % 3:59 Pm 3:09 pm 3:59 °F $1,000.10 ¢32 878¢ AFAIK £32.12 €1.01 adhd c u l8r ¥132 +1 801-520-3340 ADHD ASMR asap B4 bc bf bff brb btw c u l8r loch ness,,,,,,,       challah uh oh uhoh uh-oh"
}

# class Token:
#     def __init__(self,str,):
#         pass
#     pass

# class Delimiter(Token):
#     def __init__(self):
#         super().__init__(str)

# class Word(Token):
#     def __init__(self, text, emphasis=False):




# for pattern replacers, have an option to override the pronunciation

class Token:
    # '''Explanation'''
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return "a"
    def __str__(self):
        return "a"
    # def _


sampleSentence = Token("come @ me b1ro #gamer 100% m&m gimme a yummy ^")
# returns array that is 
# “$10.30, is the correct amount for John”
# Sentence(“$10.30, is the correct amount for John.”)
# Sentence(
#   Token(“$10.30”),
#   Token(“, ”),
#   Token(“is”),
#   Token(“ ”),
#   Token(“the”),
#   Token(“ ”),
#   Token(“correct”),
#   Token(“ ”),
#   Token(“amount”),
#   Token(“ ”),
#   Token(“for”),
#   Token(“ ”),
#   Token(“John”),
#   Token(“.”),
# )
# Sentence(
#   Token(“$10.30”), # attempt unconfuse
#   Delimiter(“, ”),
#   Word(“is”),
#   Delimiter(“ ”),
#   Word(“the”),
#   Delimiter(“ ”),
#   Word(“correct”),
#   Delimiter(“ ”),
#   Word(“amount”),
#   Delimiter(“ ”),
#   Word(“for”),
#   Delimiter(“ ”),
#   Token(“John”),
#   Delimiter(“.”),
# )

sample = Token('ä')
sample = Token("ä")

print(f"Wh{sample}t's up?")
print(f"bidirectional(\"ä\")) {unicodedata.bidirectional('ä')}")
print(f"category(\"ä\")) {unicodedata.category('ä')}")
print(f"combining(\"ä\")) {unicodedata.combining('ä')}")
print(f"decimal(\"1\")) {unicodedata.decimal('1')}")
print(f"decomposition(\"ä\")) {unicodedata.decomposition('ä')}")
print(f"digit(\"ä\")) {unicodedata.digit('⁵')}")
print(f"normalize(\"NFKC\", \"⁵\")) {unicodedata.normalize('NFKC', '⁵')}")
print(f"normalize(\"NFKC\", \"⅕\")) {unicodedata.normalize('NFKC', '⅕')}")
print(f"normalize(\"NFKC\", \"ₛ\")) {unicodedata.normalize('NFKC', 'ₛ')}")
print(f"normalize(\"NFKC\", \"º\")) {unicodedata.normalize('NFKC', 'º')}")
print(f"normalize(\"NFKC\", \"⁰\")) {unicodedata.normalize('NFKC', '⁰')}")
print(f"normalize(\"NFKC\", \"₀\")) {unicodedata.normalize('NFKC', '₀')}")
print(f"normalize(\"NFKC\", \"¹\")) {unicodedata.normalize('NFKC', '¹')}")
print(f"normalize(\"NFKC\", \"₁\")) {unicodedata.normalize('NFKC', '₁')}")
print(f"normalize(\"NFKC\", \"²\")) {unicodedata.normalize('NFKC', '²')}")
print(f"normalize(\"NFKC\", \"₂\")) {unicodedata.normalize('NFKC', '₂')}")
print(f"normalize(\"NFKC\", \"³\")) {unicodedata.normalize('NFKC', '³')}")
print(f"normalize(\"NFKC\", \"₃\")) {unicodedata.normalize('NFKC', '₃')}")
print(f"normalize(\"NFKC\", \"⁴\")) {unicodedata.normalize('NFKC', '⁴')}")
print(f"normalize(\"NFKC\", \"…\")) {unicodedata.normalize('NFKC', '…')}")
print(f"normalize(\"NFKC\", \"⁺\")) {unicodedata.normalize('NFKC', '⁺')}")
print(f"normalize(\"NFKC\", \"₊\")) {unicodedata.normalize('NFKC', '₊')}")
print(f"normalize(\"NFKC\", \"⁻\")) {unicodedata.normalize('NFKC', '⁻')}")
print(f"normalize(\"NFKC\", \"₋\")) {unicodedata.normalize('NFKC', '₋')}")
print(f"normalize(\"NFKC\", \"⁼\")) {unicodedata.normalize('NFKC', '⁼')}")
print(f"normalize(\"NFKC\", \"₌\")) {unicodedata.normalize('NFKC', '₌')}")
print(f"normalize(\"NFKC\", \"⁽\")) {unicodedata.normalize('NFKC', '⁽')}")
print(f"normalize(\"NFKC\", \"₍\")) {unicodedata.normalize('NFKC', '₍')}")
print(f"normalize(\"NFKC\", \"⁾\")) {unicodedata.normalize('NFKC', '⁾')}")
print(f"normalize(\"NFKC\", \"₎\")) {unicodedata.normalize('NFKC', '₎')}")
print(f"normalize(\"NFC\", \"⏨\")) {unicodedata.normalize('NFC', '⏨')}")
print(f"normalize(\"NFKC\", \"⏨\")) {unicodedata.normalize('NFKC', '⏨')}")
print(f"normalize(\"NFD\", \"⏨\")) {unicodedata.normalize('NFD', '⏨')}")
print(f"normalize(\"NFKD\", \"⏨\")) {unicodedata.normalize('NFKD', '⏨')}")
print(f"is_normalized(\"NFKD\", \"₎\")) {unicodedata.is_normalized('NFKD', '₎')}")

print(f"name(\"ä\")) {unicodedata.name('ä')}")
print(f"mirrored(\"ä\")) {unicodedata.mirrored('ä')}")
print(f"numeric(\"ä\")) {unicodedata.numeric('ä')}")
print(f"numeric(\"1\")) {unicodedata.numeric('1')}")
# print(f"numeric(\"⁵\")) {unicodedata.numeric("⁵")}")
# print(f"numeric(\"⅐\")) {unicodedata.numeric("⅐")}")


