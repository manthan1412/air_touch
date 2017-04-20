from settings import *
# from connect import connect
# print data


def process(matrix):
    l = len(matrix)
    matrix[0] = int(matrix[0])
    for i in range(2, l):
        if matrix[i] == '':
            matrix[i] = 0
        else:
            matrix[i] = float(matrix[i])

layer_limit = [[], [], []]

def initialize():
    data_file = open('airType_wordlist.txt', 'rb')
    global words
    words = data_file.read().split('\r\n')

    with open('prob_matrix.csv') as matrix_file:
        reader = csv.reader(matrix_file, delimiter=',')
        matrix = []
        first = True
        heading = []
        for row in reader:
            if first:
                heading = row
                first = False
            else:
                process(row)
                matrix.append(row)
        print (debug) and "\nheadings are", heading
        print (debug) and "\nmatrix created", matrix
        # process(prob_matrix)
        # print prob_matrix
    i = 2
    pairs = {'LL': i + 0, 'LR': i + 1, 'LM': i + 2, 'LI': i + 3, 'RI': i + 4, 'RM': i + 5, 'RR': i + 6, 'RL': i + 7}

    with open('layer_limit.csv') as limitFile:
        reader = csv.reader(limitFile, delimiter=',')
        i = 0
        fingers = 8
        for row in reader:
            for j in range(0, fingers):
                layer_limit[i].append((row[2*j], row[2*j + 1]))
            i += 1


    print (debug) and "\nLayer 1:",layer_limit[0]
    print (debug) and "\nLayer 2:",layer_limit[1]
    print (debug) and "\nlayer 3:",layer_limit[2]
    return heading, matrix, pairs


def from_csv():
    with open('probability.csv', 'rt') as csvfile:
        L = [list(map(float,rec)) for rec in csv.reader(csvfile, delimiter=',')]
    return L


def initialize_viterbi():
    try:
        L = from_csv()
        # print L
    except:
        L = [[0.0 for x in range(n)] for x in range(n)]
        to_csv('probability.csv', L)
    prob = [[0.0 for x in range(n)] for x in range(n)]
    return L, prob


def key_input():
    k_input = raw_input().split(' ')
    if k_input[0] == 'q' or k_input[1] == 'Q':
        k_input.append(0)
    elif k_input[0] == 'M' or k_input[0] == '1':
        if k_input[1] == 'RL':
            k_input[1] = 1

    return k_input


def get_key(item):
    return item[1]


def add_to_buffer(data):
    l = len(letter_buf)
    if l >= buffer_length:
        del letter_buf[0]
    letter_buf.append(data[0])


def smooth(i):
    j = i
    if 65 <= j and (j <= 90):
        return j - 65
    elif 97 <= j and (j <= 122):
        return j - 97
    return 0


def viterbi(letter1, letter2, action):
    i1 = ord(letter1)
    i2 = ord(letter2)
    i1 = smooth(i1)
    i2 = smooth(i2)

    #update
    if action == 'update':
        L[i1][i2] += 1
    elif action == 'undo':
        L[i1][i2] -= 1

    print (debug) and "Viterbi ", action ,"called"



def to_csv(filename, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(0, 26):
            writer.writerow(data[i])
        print "csv", filename, "created successfully"


def save_viterbi():
    for y in range(n):
        den = 1
        if sum(L[y]) > 0:
            den = sum(L[y])
        for x in range(n):
            prob[y][x] = L[y][x] / float(den)
    to_csv('probability.csv', L)
    to_csv('viterbi_probability.csv', prob)

    print (debug) and "\nViterbi saved"


def get_comb(prob_set, comb_set):
    l = len(prob_set)
    temp_set = []
    comb_len = len(comb_set)
    if comb_len == 0:
        for i in range(0, l):
            temp_set.append(prob_set[i][0])
    else:
        for i in range(0, comb_len):
            j = comb_set[i]
            for k in range(0, l):
                temp_set.append(j + prob_set[k][0])
    return comb_set + temp_set


def get_word_list(comb_set, word_list, start_value):
    set_len = len(comb_set)
    temp_list = []
    for i in range(start_value, set_len):
        regex = re.compile("\A("+ comb_set[i] + ").*")
        temp_list += [m.group(0) for l in word_list for m in [regex.search(l)] if m]

    return set_len, temp_list


def predict(combinations, first):
    input_layer, input_finger = key_input()
    if input_finger == 0:
        save_viterbi()
        return False, combinations, first
    elif input_finger == 1:
        print (debug) and "request for backspace"
        l = len(letter_buf)
        if letter_buf > 0:
            last = letter_buf.pop()
            print (debug) and "Last : ", last
            if letter_buf > 1:
                previous = letter_buf[l - 2]
                print (debug) and "previous : ", previous
                viterbi(last, previous, 'undo')
            print (debug) and "Current buffer: ", letter_buf
        if l == 1:
            first = True
        return True, combinations, first
    

    index = indices[input_finger]
    head = 19
    tail = 26
    if input_layer == '0' or input_layer == 'U':
        head = 0
        tail = 10
    elif input_layer == '1' or input_layer == 'M':
        head = 10
        tail = 19
    probability_set = []

    for i in range(head, tail):
        if prob_matrix[i][index] > 0:
            probability_set.append((prob_matrix[i][letter_index], prob_matrix[i][index]))
    try:
        probability_set = sorted(probability_set, key=get_key, reverse=True)
        print (debug) and "\nProbability set : ", probability_set
    except:
        print "You have to learn me this first"
    
    add_to_buffer(probability_set[0])
    print (debug) and "\nCurrent buffer :", letter_buf

    if not first:
        l = len(letter_buf)
        viterbi(letter_buf[l - 1], letter_buf[l - 2], 'update')
    first = False
    combinations = get_comb(probability_set, combinations)
    print combinations
    global init_value
    global words
    init_value, words = get_word_list(combinations, words, init_value)
    print words
    sets.append(probability_set)
    print sets, "\n"
    return True, combinations, first

init_value = 0
words = []
debug = True
letter_buf = []
buffer_length = 4
n = 26
headings, prob_matrix, indices = initialize()
L, prob = initialize_viterbi()

sets = []
letter_index = 1
repeat = True
first = True
comb_set = []
while repeat:
    repeat, comb_set, first = predict(comb_set, first)




