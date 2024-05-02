import time
import asyncio

import logging as log

from decouple import config
from pymodbus import Framer
from pymodbus.client import ModbusTcpClient


server_host = config('SERVER_HOST', default='upgrader')
server_port = int(config('SERVER_PORT', default='502'))
framer_type = config('FRAMER_TYPE', default='SOCKET')

match framer_type:
    case 'SOCKET':
        framer = Framer.SOCKET
    case 'ASCII':
        framer = Framer.ASCII
    case 'RTU':
        framer = Framer.RTU
    case _:
        log.fatal(f"Error: FRAMER_TYPE not in (SOCKET, ASCII, RTU):  {framer_type}")


async def run():
    client = ModbusTcpClient(
        host=server_host,
        port=server_port,
        framer=framer
    )

    client.connect()

    i = 1
    sttime = time.time()
    time.sleep(i)
    while not client.connected:
        print(f"Still connecting... elapsed time: {time.time() - sttime}")
        time.sleep(i)
        i += 1
        client.connect()
    print(f"client connection successful")


if __name__ == "__main__":
    asyncio.run(run(), debug=True)
