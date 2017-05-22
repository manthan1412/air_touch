import re
from collections import Counter

words = raw_input()

with open("all.txt") as f:
     WORDS =Counter([word for line in f for word in re.findall(r'\w+', line)])

for key,value in WORDS.items():
    print (key,value)
    
def P(word, N=sum(WORDS.values())): 
    return WORDS[word] / N

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [Left + Right[1:]               for Left, Right in splits if Right]
    transposes = [Left + Right[1] + Right[0] + Right[2:] for Left, Right in splits if len(Right)>1]
    replaces   = [Left + char + Right[1:]           for Left, Right in splits if Right for char in letters]
    inserts    = [Left + char + Right               for Left, Right in splits for char in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

print WORDS
print correction(words)


