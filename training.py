f = open('training_data.txt', 'r')
training_data = []
while True:
    ch = f.read(1)
    if not ch:
        break
    if ch.isalpha():
        training_data.append(ch)

print training_data

