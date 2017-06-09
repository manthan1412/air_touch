import serial


def connect_serial():
    try:
        ser = serial.Serial(port='COM1', baudrate=9600, bytesize=serial.EIGHTBITS , parity=serial.PARITY_NONE, timeout=1000)
        ser.isOpen()
        print('Serial port is open')
        return ser
    except:
        print('Error')
        return False


def read_serial(ser):
    if ser.isOpen():
        try:
            return ser.readline()
        except Exception:
            print "Error"
    else:
        print('COM Port cannot open')
