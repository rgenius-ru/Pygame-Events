import socket  # for socket
import sys
from time import sleep
from random import randint

value = 127
delta = 7

while True:
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_DGRAM)
        print("Socket successfully created")
    except socket.error as err:
        print(f'socket creation failed with error {err}')

    # default port for socket
    port = 80

    # try:
    #     host_ip = socket.gethostbyname('www.google.com')
    # except socket.gaierror:
    #     # this means could not resolve the host
    #     print("there was an error resolving the host")
    #     sys.exit()

    host_ip = '192.168.4.15'

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    # s.bind((host_ip, port))
    # print(f"socket binded to {port}")
    #
    # # put the socket into listening mode
    # s.listen(5)
    # print("socket is listening")

    # connecting to the server
    if s:
        s.connect((host_ip, port))
        print("the socket has successfully connected to base")
        print(f'on port == {port} and ip == {host_ip}')

        if value > 255:
            value = 255
        elif value < 0:
            value = 0

        value += randint(-delta, delta)
        string = f'left {value}\r'
        data = bytes(string, 'utf8')  # bytes('Python, bytes', 'utf8')
        # data = [randint(0, 255)]
        # data = bytes(data)
        s.sendall(data)
        # s.sendto(data, (host_ip, port))
        print(string)

        # receive data from the server
        # answer = s.recv(1024)
        # answer = hex(answer)
        # print(answer)

        s.close()

        sleep(1)
