from serial_read import *
from create_layer_data import *
import csv

f = open('training_data.txt', 'r')
training_data = []
while True:
    ch = f.read(1)
    if not ch:
        break
    if (ch.isalpha()) or (ch == '+'):
        training_data.append(ch.lower())

print training_data
layers = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

layer_data = get_layer_data(layers, training_data)
print layer_data

ser = connect_serial()

layer_limit = [[], [], []]
heading = ['LETTER', 'LAYER', "LL", "LR", "LM", "LI", "RI", "RM", "RR", "RL", "Total_Occurances"]
occurance_data = []
i = 0
str = "qwertyuiopasdfghjklzxcvbnm"
pair = {}


def make_pair():
    j = 0
    for letter in str:
        pair[letter] = j
        j += 1


def populate_iv(data):
    letters = 26
    attr = 9
    for i in range(0, letters):
        temp_list = []
        for j in range(0, attr):
            temp_list.append(0)
        data.append(temp_list)
    return data


def update_occurance_data(letter, finger):
    index = pair[letter]
    occurance_data[index][finger] += 1
    occurance_data[index][8] += 1


def initialize_layer_limit():
    for i in range(0, 3):
        for j in range(0, 8):
            layer_limit[i].append((2000, 0))


def update_layer_limit(layer, finger, angle):
    curr_min = layer_limit[layer][finger][0]
    curr_max = layer_limit[layer][finger][1]
    if curr_min > angle:
        layer_limit[layer][finger] = (angle, layer_limit[layer][finger][1])
    if curr_max < angle:
        layer_limit[layer][finger] = (layer_limit[layer][finger][0], angle)


def get_layer_limit(layer, finger=None):
    if finger is not None:
        return layer_limit[layer][finger][0], layer_limit[layer][finger][1]
    min, max = 2000, 0
    for i in range(0, 8):
        if min > layer_limit[layer][i][0]:
            min = layer_limit[layer][i][0]
        if max < layer_limit[layer][i][1]:
            max = layer_limit[layer][i][1]
    return min, max


def get_layer(letter):
    if letter in layers[0]:
        return 0
    if letter in layers[1]:
        return 1
    if letter in layers[2]:
        return 2
    return -1


def to_csv():
    with open('occurances.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(heading)
        for i in range(0, 26):
            letter = str[i]
            layer = get_layer(letter)
            occurance_data[i].insert(0, layer)
            occurance_data[i].insert(0, letter)
            writer.writerow(occurance_data[i])
        print "csv created successfully"

    with open('layer_limit.csv', 'wb') as limitFile:
        writer = csv.writer(limitFile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        fingers = 8
        for i in range(0, 3):
            limit_list = []
            for j in range(0, fingers):
                limit_list.append(layer_limit[i][j][0])
                limit_list.append(layer_limit[i][j][1])
            writer.writerow(limit_list)

        print "Layer limit is stored successfully"



initialize_layer_limit()
make_pair()
occurance_data = populate_iv(occurance_data)
# print occurance_data
loop = True
i = 0
first = read_serial(ser)
print first
first = read_serial(ser)
print first
while loop:
    try:
        if training_data[0] == '+':
            loop = False
            break
        data_in = read_serial(ser).split(' ')
        print 0, data_in
        layer = layer_data[0]
        layer_data = layer_data[1:]
        letter = training_data[0]
        training_data = training_data[1:]
        finger = int(data_in[0])
        angle = int(data_in[1])
        update_occurance_data(letter, finger)
        update_layer_limit(layer, finger, angle)

        while True:
            data_in = read_serial(ser).split(' ')
            if data_in[0] == 'END\r\n':
                break
            angle = int(data_in[1])
            update_layer_limit(layer, finger, angle)
        print "-------------------"
        print "letter", letter
        print layer_limit[0]
        print layer_limit[1]
        print layer_limit[2]
        print "-------------------"

    except:
        loop = False


print occurance_data
to_csv()
