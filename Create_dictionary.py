import re
from collections import Counter
import csv

with open("all.txt") as f:
    WORDS =Counter([word.lower() for line in f for word in re.findall(r'\w+', line)])

print WORDS
def to_csv():
    c = 0
    with open('dictionary.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for key,value in WORDS.items():
            #print key,value
            k = key.lower()
            if k.isalpha():
                c += 1
                writer.writerow([k, value])
        print "csv created successfully"
        print "count = ", c
to_csv()
