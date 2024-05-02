import logging as log
# import time

from pymodbus import __version_full__ as modbus_version
from pymodbus import pymodbus_apply_logging_config
from pymodbus.datastore.remote import RemoteSlaveContext
from pymodbus.datastore import ModbusServerContext
from pymodbus.client import ModbusTcpClient, AsyncModbusTcpClient
from pymodbus.server import ModbusTlsServer, StartAsyncTlsServer
from pymodbus.device import ModbusDeviceIdentification


class MbusUpgrader:
    msg_count: int = 1
    server: ModbusTlsServer = None
    client: AsyncModbusTcpClient = None
    context: ModbusServerContext = None

    def __init__(self, listen_port, server_host, server_port,
                 listen_framer, server_framer, certfile_path, keyfile_path,
                 num_slaves=0, ignore_missing_slaves=True, broadcast_enable=False,
                 device_name='Modbus Upgrader', listen_host=''):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.listen_addr = (listen_host, listen_port)
        self.server_host = server_host
        self.server_port = server_port
        self.server_address = (server_host, server_port)
        self.listen_framer = listen_framer
        self.server_framer = server_framer
        self.certfile_path = certfile_path
        self.keyfile_path = keyfile_path
        self.num_slaves = num_slaves
        self.ignore_missing_slaves = ignore_missing_slaves
        self.broadcast_enable = broadcast_enable
        self.device_name = device_name
        self.identity = self.build_identity()

    async def run(self):
        pymodbus_apply_logging_config(log.DEBUG)
        self.client = AsyncModbusTcpClient(
            host=self.server_host,
            port=self.server_port,
            server_hostname=self.server_host,
            framer=self.server_framer
        )
        await self.client.connect()
        # i = 1
        # sttime = time.time()
        # time.sleep(i)
        # while not self.client.connected:
        #     print(f"upgrader -> server | conn still waiting:  {time.time() - sttime}")
        #     time.sleep(i)
        #     i += 0.5
        #     self.client.connect()
        self.context = self.build_context()

        self.server = await StartAsyncTlsServer(context=self.context,
                                                identity=self.identity,
                                                address=self.listen_addr,
                                                framer=self.listen_framer,
                                                certfile=self.certfile_path,
                                                keyfile=self.keyfile_path,
                                                ignore_missing_slaves=self.ignore_missing_slaves,
                                                broadcast_enable=self.broadcast_enable)

    def build_context(self):
        if self.num_slaves:
            store = {}
            for i in range(self.num_slaves):
                store[i.to_bytes(1, 'big')] = RemoteSlaveContext(self.client, slave=i)
            single = False
        else:
            store = RemoteSlaveContext(self.client, slave=1)
            single = True
        context = ModbusServerContext(slaves=store, single=single)
        return context

    def build_identity(self):
        return ModbusDeviceIdentification(
            info_name={
                "VendorName": "Pymodbus",
                "ProductCode": "PM",
                "ProductName": self.device_name,
                "ModelName": self.device_name,
                "MajorMinorRevision": modbus_version,
            }
        )


if __name__ == "main":
    log.fatal('Error: not a main file')
