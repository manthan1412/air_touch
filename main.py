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
    data_file = open('words.txt', 'r+')
    global words
    words = data_file.read().split('\n')

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
        print heading
        print matrix
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
    print layer_limit[0]
    print layer_limit[1]
    print layer_limit[2]
    return heading, matrix, pairs


def key_input():
    return raw_input().split(' ')


def get_key(item):
    return item[1]


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


def predict(combanations):
    input_layer, input_finger = key_input()
    if input_layer == 'q':
        return False, combanations
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
    except:
        print "You have to learn me this first"
    combanations = get_comb(probability_set, combanations)
    print combanations
    global init_value
    global words
    init_value, words = get_word_list(combanations, words, init_value)
    print words
    sets.append(probability_set)
    print sets
    return True, combanations

init_value = 0
words = []
headings, prob_matrix, indices = initialize()
sets = []
letter_index = 1
repeat = True
comb_set = []
while repeat:
    repeat, comb_set = predict(comb_set)




