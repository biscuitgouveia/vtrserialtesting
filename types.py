import serial
from time import sleep

com = serial.Serial()
com.baudrate = 38400
com.port = "COM1"
com.parity = serial.PARITY_ODD
com.stopbits = serial.STOPBITS_ONE
com.bytesize = serial.EIGHTBITS

sleep(2)

com.open()

com.write(bytearray.fromhex((0x02, 0x02, 0x10, 0x01, 0xEF)))

capture = com.read(20)

com.close()

print(capture)



# Sense request = 0x6, Status sense = 0x20