from decouple import config
from pymodbus.client import ModbusSerialClient


server_host = config('SERVER_HOST', default='localhost')
server_port = int(config('SERVER_PORT', default='502'))

serial_port = int(config('SERIAL_PORT', default='502'))
baudrate = int(config('BAUDRATE', default=9600))
bytesize = int(config('BYTESIZE', default=8))
stop_bits = int(config('STOPBITS', default=1))
parity = config('PARITY', 'N')