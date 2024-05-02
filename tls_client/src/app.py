import time
import asyncio
import statistics

import logging as log

from decouple import config
from pymodbus import Framer, ModbusException
from pymodbus.client import ModbusTlsClient, AsyncModbusTlsClient


server_host = config('SERVER_HOST', default='upgrader')
server_port = int(config('SERVER_PORT', default='502'))

certfile_path = config('CERTFILE_PATH', default='/certs/example.crt')
keyfile_path = config('KEYFILE_PATH', default='/certs/example.key')

framer = Framer.TLS


def stats(rw_times):
    maxx = 0
    minn = 0
    for i in rw_times:
        if i > maxx:
            maxx = i
        elif 0 < i < minn:
            minn = i
    return maxx, minn


async def run():
    # client = ModbusTlsClient(
    #     host=server_host,
    #     port=server_port,
    #     framer=framer,
    #     certfile=certfile_path,
    #     keyfile=keyfile_path
    # )

    client = AsyncModbusTlsClient(
        host=server_host,
        port=server_port,
        framer=framer,
        certfile=certfile_path,
        keyfile=keyfile_path
    )

    await client.connect()

    # i = 1
    # sttime = time.time()
    # time.sleep(i)
    # while not client.connected:
    #     print(f"Still connecting... elapsed time: {time.time() - sttime}")
    #     time.sleep(i)
    #     i += 1
    #     client.connect()
    # print(f"client connection successful")

    rw_times = []
    i = 0
    while i < 5:
        el = await run_some(client)
        if el:
            rw_times.append(el)
        time.sleep(1)
        i += 1
    client.close()
    maxx, minn = stats(rw_times)
    print(f"rw_times: {rw_times}")
    print(f"mean:    {statistics.mean(rw_times)}")
    print(f"stddev:  {statistics.stdev(rw_times)}")
    print(f"max:     {maxx}")
    print(f"min:     {minn}")


async def run_some(client):
    try:
        sttime = time.time()
        rr = await client.read_coils(32, 1, slave=1)
        # log.info(f"rr:  {rr}")
        assert len(rr.bits) == 8
        rr = await client.read_holding_registers(4, 2, slave=1)
        elapsed = time.time() - sttime
        # log.info(f"rr: {rr}")
        assert rr.registers[0] == 17
        assert rr.registers[1] == 17
        return elapsed
    except ModbusException as e:
        print(f"error: {e}")


if __name__ == "__main__":
    asyncio.run(run(), debug=True)
