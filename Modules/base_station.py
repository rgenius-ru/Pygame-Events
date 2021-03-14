import serial
import glob
import sys
from threading import Thread
import threading
import time


class SearchingBase(Thread):
    def __init__(self, port=None, ports=None, baud=115200):
        super().__init__()
        self.baud = baud
        self._ports = ports
        self.port = port
        self.received_data = None
        self.is_connected = False
        self._running = True

    def run(self):
        s, port = self._searching_base_station()
        while self._running:
            self.receive()

    def stop(self):
        self._running = False

    def receive(self):
        if self.is_connected:
            try:
                _serial = serial.Serial(self.port, self.baud, )
                self.received_data = self._wait_receive(_serial, self.port)
            except serial.SerialException as e:
                if e.errno == 13:
                    print('e')
                    raise e
                return None
            except OSError:
                print('OSError')
                return None

            return self.received_data

        return None

    def _wait_receive(self, _serial, _port, _timeout=1):
        _serial = serial.Serial(_port, self.baud, timeout=_timeout)
        _string = None

        if _serial.isOpen():
            # while not _serial.inWaiting():
            #     pass

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
                    _s = serial.Serial(_port, self.baud, timeout=4)

                    if _s.isOpen():
                        data = bytes('Game-Event\r', 'utf8')
                        _s.write(data)

                        _data_read = _s.read(20)
                        _string = _data_read.decode('utf8')

                        # print(_string)
                        if _string[:-5] == 'Event-Game-base':
                            self.port = _port
                            self.is_connected = True
                            result = _s, _port
                            print('Found: ', _string)
                            return result

                    _s.close()
                except UnicodeEncodeError as err:
                    self.port = None
                    self.is_connected = False
                    print('Base station not found')
                    print('ERROR:', err)
                    return None, None
                except serial.SerialException as e:
                    if e.errno == 13:
                        raise e
                    self.port = None
                    self.is_connected = False
                    print('Base station not found')
                    return None, None
                except OSError:
                    self.port = None
                    self.is_connected = False
                    print('Base station not found')
                    return None, None

            self.port = None
            self.is_connected = False
            print('Base station not found')
            return None, None

        time.sleep(1)


class BaseStation(SearchingBase):
    def __init__(self):
        super().__init__()


async def print_async():
    print('hi')

if __name__ == '__main__':
    # event = threading.Event()
    base_station = BaseStation()
    base_station.start()

    while base_station.is_alive():
        time.sleep(1)

    print(base_station.baud, base_station.port)

