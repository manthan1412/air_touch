from settings import *
from serial_read import connect_serial, read_serial
## from connect import connect
## print data


def process(matrix):
    l = len(matrix)
    matrix[0] = int(matrix[0])
    for i in range(2, l):
        if matrix[i] == '':
            matrix[i] = 0
        else:
            matrix[i] = float(matrix[i])

layer_limit = [[], [], []]

##Initialize prerequisites for Model
def initialize():
    global heading
    with open('dictionary.csv', 'rb') as data_file:
        global words, word_counter
        data = csv.reader(data_file, delimiter=',')
        for row in data:
            words.append(row[0])
            word_counter[row[0]] = int(row[1])

    with open('occurrences.csv') as matrix_file:
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
        #print (debug) and "\nheadings are", heading
        #print (debug) and "\nmatrix created", matrix
        ## process(prob_matrix)
        ## print prob_matrix
    i = 2
    pairs = {'LL': i + 0, 'LR': i + 1, 'LM': i + 2, 'LI': i + 3, 'RI': i + 4, 'RM': i + 5, 'RR': i + 6, 'RL': i + 7}

    with open('layer_limit.csv') as limitFile:
        reader = csv.reader(limitFile, delimiter=',')
        i = 0
        fingers = 8
        for row in reader:
            for j in range(0, fingers):
                layer_limit[i].append((int(row[2*j]), int(row[2*j + 1])))
            i += 1


    #print (debug) and "\nLayer 1:",layer_limit[0]
    #print (debug) and "\nLayer 2:",layer_limit[1]
    #print (debug) and "\nlayer 3:",layer_limit[2]
    return heading, matrix, pairs


def from_csv():
    with open('probability.csv', 'rt') as csvfile:
        L = [list(map(float,rec)) for rec in csv.reader(csvfile, delimiter=',')]
    return L


def initialize_viterbi():
    try:
        L = from_csv()
        ## print L
    except:
        L = [[0.0 for x in range(n)] for x in range(n)]
        to_csv('probability.csv', L)
    prob = [[0.0 for x in range(n)] for x in range(n)]
    return L, prob

layer_mapping = {0: 'U', 1: 'M', 2: 'L'}
finger_mapping = {0: 'LL', 1: 'LR', 2: 'LM', 3: 'LI', 4: 'RI', 5: 'RM', 6: 'RR', 7: 'RL'}


def get_layer(finger, bending_angle):
    data = []
    for k in range(3):
        print layer_limit[k][finger]
        if bending_angle <= layer_limit[k][finger][0] and bending_angle >= layer_limit[k][finger][1]:
            l_data = []
            l_data.append(layer_mapping[k])
            l_data.append(finger_mapping[finger])
            data.append(l_data)
            #print (debug) and "layer : ", layer_mapping[k]
    return data


def approx_value(finger, bending_angle):
    layer_finger_range_list = []
    for k in range(3):
        layer_finger_range_list.append(layer_limit[k][finger][0])
        layer_finger_range_list.append(layer_limit[k][finger][1])
    approx_angle = min(layer_finger_range_list, key=lambda x:abs(x-bending_angle))
    layer_data = get_layer(finger, approx_angle)
    if len(layer_data) > 1:
        return layer_data, True
    else:
        return layer_data, False


def key_input():
    global ser, manual, finger, bending_angle, record_finger
    if manual:
        k_input = raw_input().split(' ')
        if k_input[0] == 'q' or k_input[0] == 'Q':
            k_input.append(0)
        elif (k_input[0] == 'M' or k_input[0] == '1') or k_input[1] == 'RL':
            if k_input[1] == 'RL':
                k_input[1] = 1
        elif k_input[0] == 'LTT' or k_input[0] == 'LTL':
            if len(k_input) == 1:
                k_input.append(2)
        else:
            record_finger.append(k_input[1])
            #print (debug) and "Finger Record :", record_finger
        t = []
        t.append(k_input)
        return t, False
    else:
        k_input = read_serial(ser).split(' ')
        print (debug) and k_input
        if k_input[0] == 'LTT\r\n' or k_input[0] == 'LTL\r\n' or k_input[0] == 'LTL':
            if len(k_input) == 1:
                k_input[0] = k_input[0].strip('\r\n')
                print (debug) and k_input
                k_input.append(2)
            t = []
            t.append(k_input)
            return t, False
        elif k_input[0] == '7':
            finger = int(k_input[0])
            while k_input[0] != 'END\r\n':
                k_input = read_serial(ser).split(' ')
            t = []
            k_input[0] = finger_mapping[finger]
            k_input.append(1)
            t.append(k_input)
            return t, False
        else:
            bending_angle = 0
            count = 0
            finger = int(k_input[0])
            while k_input[0] != 'END\r\n' :
                bending_angle += int(k_input[1])
                count += 1
                k_input = read_serial(ser).split(' ')
            bending_angle /= count
            print (debug) and finger, bending_angle
            #print finger_mapping[finger]
            record_finger.append(finger_mapping[finger])
            print (debug) and "Finger Record :", record_finger
            layer_data = get_layer(finger, bending_angle)
            if len(layer_data) > 1:
                return layer_data, True
            else:
                return layer_data, False


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
    return temp_set


def get_word_list(comb_set, word_list):
    set_len = len(comb_set)
    t_list = []
    temp_list = []
    for i in range(0, set_len):
        regex = re.compile("\A("+ comb_set[i] + ").*")
        t_list = [m.group(0) for l in word_list for m in [regex.search(l)] if m]
        t_list = list(sorted(t_list, key=word_counter.get, reverse=True))
        temp_list += t_list

    return temp_list


def validate_combinations(comb):
    l = len(comb)
    new_comb = []
    for k in range(l):
        try:
            i = comb[k][-1]
            j = comb[k][-2]
            ##print (debug) and ("prev : ", j , "cur : ", i, "comb", L[ascii_mapping[j]][ascii_mapping[i]])
            if int(L[ascii_mapping[j]][ascii_mapping[i]]) != 0:
                new_comb.append(comb[k])
        except:
            print "error!"
            return comb
    return new_comb


def save_dictionary():
    with open('dictionary.csv', 'wb') as dictionary:
        writer = csv.writer(dictionary, delimiter=',')
        for i in words:
            w = []
            w.append(i)
            w.append(word_counter[i])
            writer.writerow(w)


def unique_combinations(combinations):
    seen = set()
    seen_add = seen.add
    return [x for x in combinations if not (x in seen or seen_add(x))]


def reset_all():
    global current_final_index, final_list, comb_set, predicted_words, sets, record_finger, letter_buf
    current_final_index = 0
    final_list = []
    comb_set = []
    predicted_words = list(words)
    sets = []
    record_finger = []
    letter_buf = []


def predict(combinations, first):
    global predicted_words, words, record_finger
    try:
        ## if not manual:
        input_data, multi_layer = key_input()
        input_finger = input_data[0][1]
        input_layer = input_data[0][0]
        ## else:
        ##     input_layer, input_finger = key_input()
    except:
        ## if not manual:
        input_data, multi_layer = approx_value(finger, bending_angle)
        input_finger = input_data[0][1]
        input_layer = input_data[0][0]
        ## else:
        ##     input_data, input_finger = approx_value(finger, bending_angle)
        if not input_layer and input_finger:
            print "Some error "
            return True, combinations, first
    if input_finger == 0:
        save_viterbi()
        save_dictionary()
        return False, combinations, first
    elif input_finger == 1:
        last_finger = None
        try:
            last_finger = record_finger.pop()
        except:
            record_finger = []
        print (debug) and "request for backspace"
        #print (debug) and "Removed last finger :", last_finger
        l = len(letter_buf)
        if l > 0:
            last = letter_buf.pop()
            #print (debug) and "Last : ", last
            if l > 1:
                previous = letter_buf[l - 2]
                #print (debug) and "previous : ", previous
                viterbi(last, previous, 'undo')
            #print (debug) and "Current buffer: ", letter_buf
        if l == 1:
            first = True
        global sets
        try:
            sets.pop()
        except:
            sets = []
        try:
            length = len(combinations)
            for j in range(length):
                combinations[j] = combinations[j][:-1]
            combinations = unique_combinations(combinations)
            print (debug) and "new comb : ", combinations
            if len(combinations[0]) == 0:
                combinations = []
                predicted_words = list(words)
            else:
                predicted_words = get_word_list(combinations, words)
            print (debug) and "new predicted words : ", predicted_words
            print (debug) and "Last input has been discarded. Continue typing...", "\n"
        except:
            combinations = []
            predicted_words = list(words)
        return True, combinations, first
    
    elif input_finger == 2:
        global final_list, current_final_index
        if input_layer == 'LTT':
            l = len(sets)
            print "Length of the words are : ", l
            final_list = [y for x, y in enumerate(predicted_words) if len(predicted_words[x]) == l]
            final_list = final_list[:10]
            current_final_index = 0
            print final_list, "\nLong tap left thumb to select the word\n"
            return True, combinations, first

        elif input_layer == 'LTL':
            if final_list == []:
                # l = len(sets)
                # final_list = [y for x, y in enumerate(predicted_words) if len(predicted_words[x]) == l]
                # final_list = final_list[:10]
                final_list = predicted_words
            current_final_index = 0
            while input_finger != 'END' and input_finger != 'END\r\n':

                if final_list == []:
                    print "No possible words predicted"
                    break
                try:
                    current_selected_word = final_list[current_final_index]
                except:
                    current_final_index = 0
                    current_selected_word = final_list[current_final_index]
                current_final_index += 1


                print "Current selected word : ", current_selected_word
                print "Keep long pressing left thumb to iterate over the list of possible words : ", final_list
                print "Leave the left thumb to select the word : ", current_selected_word, "\n"
                input_data, multi_layer = key_input()
                input_layer = input_data[0][0]
                input_finger = input_data[0][1]
            word_counter[current_selected_word] += 1
            pair = {'LL': 2 + 0, 'LR': 2 + 1, 'LM': 2 + 2, 'LI': 2 + 3, 'RI': 2 + 4, 'RM': 2 + 5, 'RR': 2 + 6, 'RL': 2 + 7}
            number_of_finger = len(record_finger)
            for k in range(0,number_of_finger):
                    for d in range(1,27):
                        if current_selected_word[k] == prob_matrix[d][1]:
                            prob_matrix[d][pair[record_finger[k]]] += 1
                            prob_matrix[d][-1] += 1
                            break

            save_dictionary()
            with open("occurrences.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerow(headings)
                writer.writerows(prob_matrix)
            reset_all()
            print "\n selected word : ", current_selected_word, "\n Dictionary has been updated","\nStart typing ahead"
            return True, [], True

    l = len(input_data)
    if multi_layer:
        print (debug) and "Found multi layer : ", l
    probability_set = []
    for i in range(0, l):
        index = indices[input_finger]
        head = 19
        tail = 26
        input_layer = input_data[i][0]
        print (debug) and "input layer ", l, "is : ", input_layer
        if input_layer == '0' or input_layer == 'U':
            head = 0
            tail = 10
        elif input_layer == '1' or input_layer == 'M':
            head = 10
            tail = 19


        for i in range(head, tail):
            if prob_matrix[i][index] > 0:
                probability_set.append((prob_matrix[i][letter_index], prob_matrix[i][index]))
    try:
        probability_set = sorted(probability_set, key=get_key, reverse=True)
        print (debug) and "\nProbability set : ", probability_set
    except:
        print "You have to learn me this first"
    
    add_to_buffer(probability_set[0])
    #print (debug) and "\nCurrent buffer :", letter_buf

    if not first:
        l = len(letter_buf)
        viterbi(letter_buf[l - 1], letter_buf[l - 2], 'update')
    first = False
    combinations = get_comb(probability_set, combinations)
    print (debug) and "All possible combinations : ", combinations
    combinations = validate_combinations(combinations)
    print (debug) and "\nValidated combinations : ", combinations
    # global init_value
    # global words
    predicted_words = get_word_list(combinations, predicted_words)
    print "\nTop 10 possible words :",predicted_words[:11],"\n"
    sets.append(probability_set)
    #print sets, "\n"
    return True, combinations, first

# init_value = 0
words = []
manual = True
word_counter = {}
record_finger = []
debug = True
letter_buf = []
buffer_length = 4
n = 26
ascii_mapping = {}
ascii_val = 97
for i in range(0, 26):
    ascii_mapping[chr(ascii_val)] = i
    ascii_val += 1
print ascii_mapping
headings, prob_matrix, indices = initialize()
L, prob = initialize_viterbi()
print L
ser = None
if not manual:
    ser = connect_serial()
    print read_serial(ser)
    print read_serial(ser)

final_list = []
current_final_index = 0
sets = []
letter_index = 1
repeat = True
first = True
comb_set = []
predicted_words = list(words)
while repeat:
    repeat, comb_set, first = predict(comb_set, first)

