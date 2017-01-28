layers = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

layer_data = []


def get_layer_data(letters):
    for letter in letters:
        if letter in layers[0]:
            layer_data.append(0)
        elif letter in layers[1]:
            layer_data.append(1)
        elif letter in layers[2]:
            layer_data.append(2)
        else:
            layer_data.append(' ')
    return layer_data
