import commandTypes
import encoder
import binascii


def open_port(port_number=0x01, target_port="COM1", is_locked=False):

    if is_locked:
        is_locked = 0x01
    else:
        is_locked = 0x00

    packet = encoder.encode_packet(
        encoder.encode_commands(
            commandTypes.CMD1.SenseRequest.value,
            commandTypes.SenseRequestCommands.open_port.value,
            [port_number, is_locked]
                                )
    )

    target_port.write(packet)
    capture = target_port.read(50)
    print(capture)
    capture = binascii.b2a_hex(capture)
    print(capture)






print(decode_response(b'\x02\x050\x85\x01\x01\x01H'))

def decode_open_port(response):

    # Return data format:
    # 0x2, 0x3, 0x30, 0x81, DATA1, CS

    if response[4] == 0x01:
        print("Access to Port Granted")
