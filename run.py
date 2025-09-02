import eng_to_ipa as p
import re
from functions import *


# convertedText = p.ipa_list(text)
# print(p.cmu_to_ipa(text))
# throw(p.find_stress(text))
# print(p.convert(p.get_all(text)[0]))

# print(p.ipa_list(text))
# print(p.convert(p.get_top(text)))
# print(p.syllable_count(text))
# print(p.apply_punct(text))


print(unconfuse("1 apple? and 1 bread for $100.30 12:03"))

# method = input("""
# Choose your method:
# [1]: zigzag
# [2]: back to front
# [3]: front to back
# [4]: hopeless
# (Enter for default)
# """)
# if (method == ""):
#     method = 0
# else:
#     method = int(method)
#     match method:
#         case 1 | 2 | 3 | 4:
#             None
#         case _:
#             method = 0

# print(f"chose {method}")
# inputText = input("Enter some text: \n(Enter to choose)")
# if not (inputText == ""):
#     print(convert_to_pronounceable(inputText, method))
# else:
#     print("Choose a number:")
#     for i, text in enumerate(texting):
#         print(f"[{1+i}]: \"{text}\"")
#     print("(Enter for 1)")
#     userInput = input()
#     if (userInput == ""):
#         userInput = 1
#     print(convert_to_pronounceable(texting[int(userInput)-1], method))


print(p.ipa_list("tennessee"))
print(p.ipa_list("emoji"))


print(zigzag_check("wowthatiscool"))
