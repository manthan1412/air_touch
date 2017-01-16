import serial
ser = serial.Serial(port='COM1', baudrate=9600, bytesize=serial.EIGHTBITS , parity=serial.PARITY_NONE, timeout=100)
try:
    ser.isOpen()
    print('Serial port is open')
except:
    print('Error')
    exit()

if(ser.isOpen()):
    try:
        while(1):
            print(ser.readline())
    except Exception:
        print('Error')
else:
    print('COM Port cannot open')
