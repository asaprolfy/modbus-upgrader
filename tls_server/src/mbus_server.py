import logging as log

from pymodbus import pymodbus_apply_logging_config
from pymodbus.server import ModbusTlsServer  # , StartTlsServer
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock


class MbusServer:
    msg_count: int = 0
    server: ModbusTlsServer = None

    def __init__(self, context, identity, host, port, framer, certfile_path, keyfile_path,
                 ignore_missing_slaves=True, broadcast_enable=False):
        self.context = context
        self.identity = identity
        self.host = host
        self.port = port
        self.address = (host, port)
        self.framer = framer
        self.certfile_path = certfile_path
        self.keyfile_path = keyfile_path
        self.ignore_missing_slaves = ignore_missing_slaves
        self.broadcast_enable = broadcast_enable

    def request_tracer(self, request, *_addr):
        print(f"Request:  {request} | *_addr:  {_addr} | msg_count:  {self.msg_count}")

    def response_manipulator(self, response):
        if self.msg_count == 0:
            print(f"Response:  {response} | msg_count:  {self.msg_count}")
            self.msg_count = 3
        else:
            print(f"Response:  NONE | msg_count:  {self.msg_count}")
            response.should_respond = False
            self.msg_count -= 1
        return response, False

    async def setup(self):
        pymodbus_apply_logging_config(log.DEBUG)
        datablock = ModbusSequentialDataBlock(0x00, [17] * 100)
        context = ModbusServerContext(
            slaves=ModbusSlaveContext(
                di=datablock, co=datablock, hr=datablock, ir=datablock
            ),
            single=True,
        )
        self.server = ModbusTlsServer(
            context=context,
            identity=self.identity,
            address=self.address,
            framer=self.framer,
            certfile=self.certfile_path,
            keyfile=self.keyfile_path,
            ignore_missing_slaves=self.ignore_missing_slaves,
            broadcast_enable=self.broadcast_enable,
            request_tracer=self.request_tracer,
            response_manipulator=self.response_manipulator
            # host=self.host,
            # port=self.port,
        )

    async def run(self):
        await self.server.serve_forever()


if __name__ == "main":
    log.fatal('Error: not a main file')
