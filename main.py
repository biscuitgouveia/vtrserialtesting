import serial
from time import sleep
import binascii

import commandTypes
from commandBlocks import CommandBlocks


def main():

    # com.write(bytearray.fromhex((0x02, 0x02, 0x10, 0x01, 0xEF)))

    # com.write(bytearray.fromhex("0203202101be"))

    # capture = com.read(20)

    test_play = CommandBlocks()

    test_play.init_serial()

    test_play.open_port()

    test_play.get_port_status()

    test_play.serial_port.close()


if __name__ == '__main__':
    main()
