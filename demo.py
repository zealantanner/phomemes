import eng_to_ipa as ipa
# https://pypi.org/project/eng-to-ipa/
from spellchecker import SpellChecker
# https://pypi.org/project/pyspellchecker/
# https://pyspellchecker.readthedocs.io/en/latest/

spell = SpellChecker()


text = "Thnak"
print(ipa.ipa_list(text))
# print(ipa.i(text))
 
# convertedText = p.ipa_list(text)
# print(ipa.cmu_to_ipa(text))
# print(ipa.find_stress(text))
print(ipa.convert(ipa.get_all(text)[0]))
print(ipa.get_all(text))
print(spell.candidates(text))
ipa.syllable_count
# spell.
# print(spell.candidates("askin"))
# print(ipa.get_rhymes("billy"))
# misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])

# print(spell.word_usage_frequency("the"))

text = "askin"
rhymes = ipa.get_rhymes(text)




rhymes.sort(key=spell.word_usage_frequency, reverse=True)

# for word in rhymes:
#     print(word,spell.word_usage_frequency(word))




print(rhymes)