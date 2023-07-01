import serial
from time import sleep
import binascii

import commandTypes
from commandBlocks import CommandBlocks


def main():

    com = serial.Serial("COM1")
    com.baudrate = 38400
    com.parity = serial.PARITY_ODD
    com.stopbits = serial.STOPBITS_ONE
    com.bytesize = serial.EIGHTBITS
    com.timeout = 2



    # com.write(bytearray.fromhex((0x02, 0x02, 0x10, 0x01, 0xEF)))

    # com.write(bytearray.fromhex("0203202101be"))

    # capture = com.read(20)

    open_port = CommandBlocks(commandTypes.CMD1.SenseRequest.value, commandTypes.SenseRequestCommands.open_port.value)

    get_status = CommandBlocks(commandTypes.CMD1.SenseRequest.value, commandTypes.SenseRequestCommands.port_status.value)

    com.close()


if __name__ == '__main__':
    main()
