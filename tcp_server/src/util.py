from pymodbus import __version_full__ as modbus_version
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.device import ModbusDeviceIdentification


def sequential_datablock():
    return ModbusSequentialDataBlock(0x00, [17] * 100)


def sparse_datablock():
    return ModbusSparseDataBlock({0x00: 0, 0x05: 1})


def factory_datablock():
    return ModbusSequentialDataBlock.create()


def build_context(store, num_slaves):
    # match store:
    #     case 'sequential':
    #         datablock = lambda: ModbusSequentialDataBlock(0x00, [17] * 100)
    #     case 'sparse':
    #         datablock = lambda: ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     case 'factory':
    #         datablock = lambda: ModbusSequentialDataBlock.create()

    match store:
        case 'sequential':
            datablock = sequential_datablock
        case 'sparse':
            datablock = sparse_datablock
        case 'factory':
            datablock = factory_datablock
        case _:
            datablock = factory_datablock

    if num_slaves:
        slave_context = {
            0x01: ModbusSlaveContext(
                di=datablock(),
                co=datablock(),
                hr=datablock(),
                ir=datablock(),
            ),
            0x02: ModbusSlaveContext(
                di=datablock(),
                co=datablock(),
                hr=datablock(),
                ir=datablock(),
            ),
            0x03: ModbusSlaveContext(
                di=datablock(),
                co=datablock(),
                hr=datablock(),
                ir=datablock(),
                zero_mode=True,
            )
        }
        single = False
    else:
        slave_context = ModbusSlaveContext(
            di=datablock(),
            co=datablock(),
            hr=datablock(),
            ir=datablock(),
        )
        single = True

    context = ModbusServerContext(slaves=slave_context, single=single)

    identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": modbus_version,
        }
    )
    return context, identity
