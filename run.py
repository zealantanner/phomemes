import eng_to_ipa as p 
import re
from functions import *


inputText = "The world is a vampoire, and I love gobbbobagabboh"
text = split(inputText) 


convertedText = p.ipa_list(text)
# print(p.cmu_to_ipa(text))
# throw(p.find_stress(text))
# print(p.convert(p.get_all(text)[0]))

print(p.ipa_list(text))
# print(p.convert(p.get_top(text)))
# print(p.syllable_count(text))
# print(p.apply_punct(text))
print(p.isin_cmu(text))
first_half  = ""
second_half = ""


def fix_broken_words():
	for i in convertedText:
		if('*' in i[0]):
			s = cut_string_in_half(i[0])
			print(s)
			print("hello there buddy")


		# if('*' in i[0]):
			print("this word doesn't parse")

		print(first_half)
		print(second_half)
		print(i)