import time
import re
from collections import Counter

def find_word(word):
	return re.findall(r'\w+', word.lower())

def count_words(list):
	return Counter(list)
flag = 0

next_word = []

# with open('all.txt','r') as word:
#     for line in word:
#         for specific in line.split():
#             if flag == 1:
#                 next_word.append(specific.lower())
#                 flag = 0
#             if specific.lower() == 'king':
#                 flag = 1
#                 pass
#
# next_word_list = Counter(next_word)
word_list = Counter(find_word(open('all.txt').read()))
# print next_word
# print len(next_word)
# print next_word_list
print word_list.keys()
print len(word_list)

text_file = open("airType_wordlist.txt", "w")
for k in word_list.keys():
	text_file.write("%s\n"%k)
# text_file.write(line for line in word_list.keys())
text_file.close()
