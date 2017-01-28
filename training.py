from serial_read import *
from create_layer_data import *

f = open('training_data.txt', 'r')
training_data = []
while True:
    ch = f.read(1)
    if not ch:
        break
    if ch.isalpha():
        training_data.append(ch.lower())

print training_data
layer_data = get_layer_data(training_data)
print layer_data

ser = connect_serial()

layer_limit = [[], [], []]


def initialize_layer_limit():
    for i in range(0, 3):
        for j in range(0, 8):
            layer_limit[i].append((2000, 0))


def update_layer_limit(layer, finger, angle):
    curr_min = layer_limit[layer][finger][0]
    curr_max = layer_limit[layer][finger][1]
    if curr_min > angle:
        layer_limit[layer][finger][0] = angle
    if curr_max < angle:
        layer_limit[layer][finger][1] = angle

initialize_layer_limit()
loop = True
i = 0
while loop:
    try:
        data_in = read_serial(ser).split(' ')
        layer = layer_data.pop()
        letter = training_data.pop()
        finger = data_in[0]
        angle = data_in[1]
        update_layer_limit(layer, finger, angle)

        while data_in != 'END':
            data_in = read_serial(ser).split(' ')
            angle = data_in[1]
            update_layer_limit(layer, finger, angle)
    except:
        loop = False

