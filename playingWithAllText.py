import eng_to_ipa as p 
import re
import functions



allText = open("allText.txt", 'r')
# yourResult = [line.split(',') for line in allText.readlines()]
lines = allText.readlines()
lines = [functions.split(line, "\t(")[0] for line in lines]
lines = list(dict.fromkeys(lines))
lines = sorted(lines, key=lambda x: -len(x))
for i, line in enumerate(lines[:300]):
	print(f"{i+1}:\t\"{line}\"")

print(len(lines[0]))
print(len(lines[1]))