import time
import asyncio

import logging as log

from decouple import config
from pymodbus import Framer, ModbusException
from pymodbus.client import ModbusTlsClient


server_host = config('SERVER_HOST', default='upgrader')
server_port = int(config('SERVER_PORT', default='502'))

certfile_path = config('CERTFILE_PATH', default='/certs/example.crt')
keyfile_path = config('KEYFILE_PATH', default='/certs/example.key')

framer = Framer.TLS


async def run():
    client = ModbusTlsClient(
        host=server_host,
        port=server_port,
        framer=framer,
        certfile=certfile_path,
        keyfile=keyfile_path
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
    i = 0
    while i < 200:
        run_some(client)
        time.sleep(1)
        i += 1
    client.close()


def run_some(client):
    try:
        rr = client.read_coils(32, 1, slave=1)
        log.info(f"rr:  {rr}")
        assert len(rr.bits) == 8
        rr = client.read_holding_registers(4, 2, slave=1)
        log.info(f"rr: {rr}")
        assert rr.registers[0] == 17
        assert rr.registers[1] == 17
    except ModbusException as e:
        print(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(run(), debug=True)
