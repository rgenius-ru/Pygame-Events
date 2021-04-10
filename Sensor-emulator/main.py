import socket  # for socket
from time import sleep
from random import randint

value_left = 127
value_right = 127
delta = 40


def constrain(number, _min, _max):
    if number > _max:
        result = _max
    elif number < _min:
        result = _min
    else:
        result = number

    return result


def send_data(_socket, _string):
    _data = bytes(_string, 'utf8')  # bytes('Python, bytes', 'utf8')

    try:
        _socket.sendall(_data)
    except socket.error as _err:
        print(f'socket creation failed with error {_err}')

    print(_string)


def send_l_or_r(side: str):
    global value_left, value_right
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_DGRAM)
    except socket.error as err:
        print(f'socket creation failed with error {err}')

    port = 80
    host_ip = '192.168.4.15'

    if s:
        try:
            s.connect((host_ip, port))
        except socket.error as err:
            print(f'socket creation failed with error {err}')

        value = None
        if side == 'l':
            value_left += randint(-delta, delta)
            value_left = constrain(value_left, 100, 255)
            value = value_left
        elif side == 'r':
            value_right += randint(-delta, delta)
            value_right = constrain(value_right, 100, 255)
            value = value_right
        else:
            s.close()
            return False

        string = side + str(value) + '\r'
        send_data(s, string)

        s.close()
        return True


while True:
    send_l_or_r('l')
    sleep(0.2)
    send_l_or_r('r')
    sleep(0.2)
