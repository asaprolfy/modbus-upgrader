import logging as log
import asyncio

from decouple import config
from pymodbus.framer import Framer

from util import build_context
from mbus_server import MbusServer

host = config('SERVER_HOSTNAME', default='localhost')
port = int(config('SERVER_PORT', default='502'))
address = (host, port)

certfile_path = config('CERTFILE_PATH', default='../../certs/modbus.crt')
keyfile_path = config('KEYFILE_PATH', default='../../certs/modbus.key')

store = config('STORE', default='factory')
num_slaves = int(config('NUM_SLAVES', default='0'))
ignore_missing_slaves = bool(config('IGNORE_MISSING_SLAVES', default='True'))
broadcast_enable = bool(config('BROADCAST_ENABLE', default='False'))

framer = Framer.TLS


# def start_server():
#     context, identity = build_context(store, num_slaves)
#     mbus_server = StartTlsServer(
#         context=context,
#         identity=identity,
#         address=address,
#         host=host,
#         port=port,
#         framer=framer,
#         certfile=certfile_path,
#         keyfile=keyfile_path,
#         ignore_missing_slaves=ignore_missing_slaves,
#         broadcast_enable=broadcast_enable
#     )
#     return mbus_server


async def main():
    context, identity = build_context(store, num_slaves)
    server = MbusServer(
        context=context,
        identity=identity,
        host=host,
        port=port,
        framer=framer,
        certfile_path=certfile_path,
        keyfile_path=keyfile_path,
        ignore_missing_slaves=ignore_missing_slaves,
        broadcast_enable=broadcast_enable
    )
    await server.setup()
    await server.run()


if __name__ == "__main__":
    # server: ModbusTlsServer = start_server()
    asyncio.run(main(), debug=True)
