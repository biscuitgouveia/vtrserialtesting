import serial
from time import sleep
import binascii

com = serial.Serial("COM1")
com.baudrate = 38400
com.parity = serial.PARITY_ODD
com.stopbits = serial.STOPBITS_ONE
com.bytesize = serial.EIGHTBITS
com.timeout = 2

sleep(2)


# com.write(bytearray.fromhex((0x02, 0x02, 0x10, 0x01, 0xEF)))

com.write(bytearray.fromhex("0203202101be"))

capture = com.read(20)

com.close()

print(capture)
new = binascii.b2a_hex(capture)
print(new)
