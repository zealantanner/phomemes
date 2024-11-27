import eng_to_ipa as p 
import re

periodPauseDelimiters = ".!&?\n"
commaPauseDelimiters  = ",~*()=+\\:;\""
spacePauseDelimiters  = " -_></"
delimiters = periodPauseDelimiters+commaPauseDelimiters+spacePauseDelimiters
def split(string:str, delimiters=delimiters, maxsplit=0):
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)
def flatten(S):
	if S == []:
		return S
	if isinstance(S[0], list):
		return flatten(S[0]) + flatten(S[1:])
	return S[:1] + flatten(S[1:])





def replace_delimiters1(token:str):
	period= re.escape(periodPauseDelimiters)
	comma = re.escape(commaPauseDelimiters)
	space = re.escape(spacePauseDelimiters)
	
	periodDelimiters = r"[^" + period + "]*[" + period + "]+[^" + period + "]*"
	commaDelimiters  = r"[^" + comma  + "]*[" + comma  + "]+[^" + comma  + "]*"
	spaceDelimiters  = r"[^" + space  + "]*[" + space  + "]+[^" + space  + "]*"
	
	# token = token.lstrip(re.escape(delimiters))
	token = re.sub(periodDelimiters,".",token)
	token = re.sub(commaDelimiters,",",token)
	token = re.sub(spaceDelimiters," ",token)
	return token

def replace_delimiters(text:str):
	text = text.lstrip(re.escape(delimiters))
	return [replace_delimiters1(token) for token in re.split(r"\b",text) if token!=""]
# apply


def is_delimiter(text:str):
	return any(elem in text for elem in delimiters)
def is_word(s):
	return (p.isin_cmu(s) and len(s)>0 and not is_delimiter(s))

testtext = [
	"Once applebananacherroy there     was a ????????????\\|(so-called) rock. it.,was not! in fact, a big rock.",
	"applebananacherry",
	"applesorangesandbananas",
	"appleorangebanana",
	"a",
	"abe",
	"IaskedasimilarquestionhereandtheanswergivendoesuseanyimportsorcomprehensionsItdoeshaveaforloopthoughAnyparticularlyreasonforthatrequirement",
	"neighbourhood vs neighborhood In sem justo, commodo ut, suscipit at, pharetra vitae, orci. Duis sapien nunc, commodo et, interdum suscipit, sollicitudin et, dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam id dolor. Class aptent taciti sociosqu ad litora",
	"ThatsoneofthetopresultswhenIlookupwiitank",
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
    
def zigzag_split_and_check(string):
	length = len(string)
	mid = length // 2
	offsets = [0]

	for i in range(1, mid + 1):
		offsets.append(i)
		offsets.append(-i)

	offsets = sorted(set(offsets), key=abs)
	results = []
	# results.append((left, right))

	for offset in offsets:
		left = string[:mid + offset]
		right = string[mid + offset:]
		print(f"Checking: {left}|{right}")
		# print(f"offset: {offset}")
		if is_word(left):
			results.append(left)
			print(f"Valid word: \"{left}\"")
			if is_word(right):
				results.append(right)
				print(f"Valid word: \"{right}\"")
				break
			else:
				results.append(zigzag_split_and_check(right))
			break
	return flatten(results)


# def fix_broken_word(word:str):
# 	array = []
# 	# text = split(text)
# 	if(not p.isin_cmu(word)):
# 		for
# 		word[:len(word)//2], word[len(word)//2:]

# 	# for i in text:
# 		# print(i)
# 		if(p.isin_cmu(text)):
# 			# s = cut_string_in_half(i[0])
# 			# print(s)
# 			# print("hello there buddy")


# 		# if('*' in i[0]):
# 			print("this word doesn't parse")

# 		# print(first_half)
# 		# print(second_half)
# 		# print(i)
# 	return []



def convert_to_pronouncable(text:str):
	t = text
	t = replace_delimiters(t)
	newText = []
	for word in t:
		if(is_delimiter(word) or is_word(word)):
			newText.append(word)
		else:
			newText.append((zigzag_split_and_check(word)))
	print(text)
	return flatten(newText)

#to do: the split, check, zig, check, zag, check

# print(testtext)
# print(special_split(testtext))
# print('|'.join(map(re.escape, delimiters)))
# text3 = "yo ur cant"

# print([replaceDelimiters(token) for token in re.split(r"\b",text3)])
# print(replaceDelimiters(text3))
# for the in replaceDelimiters(text3):
# 	if(not isDelimiter(the)):
# 		print(the, " = ", p.isin_cmu(the))
# print(["asdf", cut_string_in_half("text3")])
# print(zigzag_split_and_check(testtext[8]))
# print(convert_to_pronouncable(testtext[8]))
# print(replaceDelimiters(text3))
# print(p.isin_cmu(text3))
# print(p.ipa_list(text3))
print(convert_to_pronouncable(input("Enter some text: ")))
