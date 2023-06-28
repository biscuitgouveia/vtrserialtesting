import binascii


def encode_commands(command_1, command_2, data=None):

    packet_content = bytearray()

    packet_content.append(command_1)
    packet_content.append(command_2)

    if data:
        for bit in data:
            packet_content.append(bit)

    return packet_content


def checksum(packet_content):

    data_sum = 0

    for data in packet_content:
        data_sum += data

    data_sum = -(data_sum % 256)

    return '%2X' % (data_sum & 0xFF)


def encode_packet(packet_content):

    packet = bytearray()
    bit_count = len(packet_content)
    checksum_value = int(checksum(packet_content), 16)

    packet.append(0x02)
    packet.append(bit_count)
    packet = packet + packet_content
    packet.append(checksum_value)

    return packet


test_case = encode_commands(0x30, 0x85, [0x01, 0x01, 0x01])

print(encode_packet(test_case))
