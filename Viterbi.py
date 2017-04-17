import csv

def to_csv(filename, data):
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for i in range(0, 26):
			writer.writerow(data[i])
		print "csv", filename, "created successfully"


def from_csv():
    with open('probability.csv', 'rt') as csvfile:
        L = [list(map(float,rec)) for rec in csv.reader(csvfile, delimiter=',')]
    return L


def smooth(i):
    j = i
    if 65 <= j and (j <= 90):
        return j - 65
    elif 97 <= j and (j <= 122):
        return j - 97
    return 0

def probability_to_csv():
	with open('viterbi_probability.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for i in range(0, 26):
			writer.writerow(prob[i])
		print "Viterbi Probability matrix created successfully"


n = 26
try:
    L = from_csv()
    # print L
except:
    L = [[0.0 for x in range(n)] for x in range(n)]
    to_csv('probability.csv', L)


string = raw_input()
prob = [[0.0 for x in range(n)] for x in range(n)]

while 1:
    if string != 'exit':
        for i in range(1,len(string)):
            i1 = ord(string[i - 1])
            i2 = ord(string[i])
            i1 = smooth(i1)
            i2 = smooth(i2)
            L[i1][i2]+=1
        
        string = raw_input()
    else:
        for y in range(n):
            if sum(L[y]) == 0:
                    denom = 1
            else:
                denom = sum(L[y])
            for x in range(n):
                
                prob[y][x] = L[y][x]/float(denom)
        to_csv('probability.csv', L)
        to_csv('viterbi_probability.csv', prob)
        break


