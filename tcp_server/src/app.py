import logging as log
import asyncio

from decouple import config
from pymodbus.framer import Framer

from util import build_context
from mbus_server import MbusServer

host = config('SERVER_HOSTNAME', default='')
port = int(config('SERVER_PORT', default='502'))
address = (host, port)
framer_type = config('FRAMER_TYPE', default='SOCKET')

store = config('STORE', default='factory')
num_slaves = int(config('NUM_SLAVES', default='0'))
ignore_missing_slaves = bool(config('IGNORE_MISSING_SLAVES', default='True'))
broadcast_enable = bool(config('BROADCAST_ENABLE', default='False'))

match framer_type:
    case 'SOCKET':
        framer = Framer.SOCKET
    case 'ASCII':
        framer = Framer.ASCII
    case 'RTU':
        framer = Framer.RTU
    case _:
        log.fatal(f"Error: FRAMER_TYPE not in (SOCKET, ASCII, RTU):  {framer_type}")


async def main():
    context, identity = build_context(store, num_slaves)
    server = MbusServer(
        context=context,
        identity=identity,
        host=host,
        port=port,
        framer=framer,
        ignore_missing_slaves=ignore_missing_slaves,
        broadcast_enable=broadcast_enable
    )
    await server.setup()
    await server.run()


if __name__ == "__main__":
    # server: ModbusTlsServer = start_server()
    asyncio.run(main(), debug=True)
