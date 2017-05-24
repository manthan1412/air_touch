import re
from collections import Counter
import csv

with open("all.txt") as f:
     WORDS =Counter([word for line in f for word in re.findall(r'\w+', line)])
	 
def to_csv():
     with open('dictionary.csv', 'wb') as csvfile:
         writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
         for key,value in WORDS.items():
             #print key,value
             writer.writerow([key,value])
         print "csv created successfully"

to_csv()
