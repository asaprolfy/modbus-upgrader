import asyncio

from decouple import config

from pymodbus.framer import Framer

from mbus_upgrader import MbusUpgrader


server_host = config('SERVER_HOST', default='localhost')
server_port = int(config('SERVER_PORT', default='502'))

listen_host = config('LISTEN_HOST', default='')
listen_port = int(config('LISTEN_PORT', default='5020'))
server_framer_type = config('SERVER_FRAMER_TYPE', default='SOCKET')
store = config('STORE', default='factory')
num_slaves = int(config('NUM_SLAVES', default='0'))
ignore_missing_slaves = bool(config('IGNORE_MISSING_SLAVES', default='True'))
broadcast_enable = bool(config('BROADCAST_ENABLE', default='False'))

certfile = config('CERTFILE_PATH', default='/certs/example.crt')
keyfile = config('KEYFILE_PATH', default='/certs/example.key')

match server_framer_type:
    case 'SOCKET':
        server_framer = Framer.SOCKET
    case 'RTU':
        server_framer = Framer.RTU
    case 'ASCII':
        server_framer = Framer.ASCII
    case _:
        server_framer = Framer.SOCKET

listen_framer = Framer.TLS


async def main():
    upgrader = MbusUpgrader(
        listen_port=listen_port,
        listen_host=listen_host,
        listen_framer=listen_framer,
        server_host=server_host,
        server_port=server_port,
        server_framer=server_framer,
        certfile_path=certfile,
        keyfile_path=keyfile,
        num_slaves=num_slaves,
        ignore_missing_slaves=ignore_missing_slaves,
        broadcast_enable=broadcast_enable
    )
    await upgrader.run()


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
