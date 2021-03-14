import serial
import glob
import sys
from threading import Thread
import threading


class BaseStation(Thread):
    def __init__(self, port=None, ports=None, baud=115200):
        super().__init__()
        self._baud = baud
        self._ports = ports
        self._port = port
        self._received_data = None
        self._is_connected = False

    def run(self):
        s, port = self._searching_base_station()

    def receive(self):
        if self._is_connected:
            try:
                _serial = serial.Serial(self._port, self._baud, )
                self._received_data = self._wait_receive(_serial, self._port)
            except serial.SerialException as e:
                if e.errno == 13:
                    print('e')
                    raise e
                return None
            except OSError:
                print('OSError')
                return None

            return self._received_data

        return None

    def _wait_receive(self, _serial, _port, _timeout=1):
        _serial = serial.Serial(_port, self._baud, timeout=_timeout)
        _string = None

        if _serial.isOpen():
            while not _serial.inWaiting():
                pass

            data_read = _serial.readline()
            try:
                _string = data_read.decode('utf8').strip()
            except UnicodeEncodeError as err:
                print('ERROR:', err)

        return _string

    def _all_serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyUSB*')  # ubuntu is /dev/ttyUSB0
            ports += glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            # ports = glob.glob('/dev/tty.*')
            ports = glob.glob('/dev/tty.SLAB_USBtoUART*')
        else:
            raise EnvironmentError('Unsupported platform')
        self._ports = ports

        return self._ports is not None

    def _searching_base_station(self):
        print('Base station search...')
        while True:
            if not self._all_serial_ports():
                continue

            ports_count = len(self._ports)
            print(f'Found {ports_count} ports: ', '  '.join(self._ports))

            for _port in self._ports:
                # if _port[:-1] == '/dev/ttyUSB':
                #     continue

                print('Scan port: ', _port)

                try:
                    _s = serial.Serial(_port, self._baud, timeout=4)

                    if _s.isOpen():
                        data = bytes('Game-Event\r', 'utf8')
                        _s.write(data)

                        _data_read = _s.read(20)
                        _string = _data_read.decode('utf8')

                        # print(_string)
                        if _string[:-5] == 'Event-Game-base':
                            self._port = _port
                            self._is_connected = True
                            result = _s, _port
                            print('Found: ', _string)
                            return result

                    _s.close()
                except UnicodeEncodeError as err:
                    self._port = None
                    self._is_connected = False
                    print('Base station not found')
                    print('ERROR:', err)
                    return None, None
                except serial.SerialException as e:
                    if e.errno == 13:
                        raise e
                    self._port = None
                    self._is_connected = False
                    print('Base station not found')
                    return None, None
                except OSError:
                    self._port = None
                    self._is_connected = False
                    print('Base station not found')
                    return None, None

            self._port = None
            self._is_connected = False
            print('Base station not found')
            return None, None


if __name__ == '__main__':
    # event = threading.Event()
    base_serial_socket = BaseStation()
    base_serial_socket.start()

    while True:
        string_data = base_serial_socket.receive()
        if string_data:
            print(string_data)
