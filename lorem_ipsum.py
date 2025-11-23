#this has been taken from https://lorem-text.readthedocs.io/en/latest/readme/#features
# comment out the options you don't want to execute for any given output run

from lorem_text import lorem

# For randomly generated sentence of lorem ipsum text where the first word is capitalized, and the sentence ends in either a period or question mark:
print(lorem.sentence())

# Generate multiple paragraphs of lorem ipsum text each paragraph’s consists of 2 to 4 sentences:
paragraph_length = 5
print(lorem.paragraphs(paragraph_length))

# Generate random lorem ipsum words seperated with single space:
words = 10
print(lorem.words(words))

#Generate a single sentence of lorem ipsum
sentence = lorem.sentence()
print(sentence)
print("this is the character count of the sentence",len(sentence), '\n')

#Generate specific number of words of lorem ipsum
word_number = 12
words = lorem.words(word_number)
print(words)
print("The number of words is",word_number,"with a character total of",len(words),'\n')

#Generate a single paragraph of lorem ipsum
paragraph = lorem.paragraph()
print(paragraph)
print("this is the character count of the paragraph",len(paragraph),'\n')

#Generate multiple paragraphs of lorem ipsum
paragraph_number = 2
paragraphs = lorem.paragraphs(paragraph_number)
print(paragraphs)
print("this is the character count of the paragraphs",len(paragraphs), '\n')