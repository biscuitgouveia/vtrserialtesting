import commandTypes
import encoder
import binascii
import main
from decoder import Decoder
from statusCodes import StatusCodes
from bitstring import Bits, BitArray, BitStream, pack


class CommandBlocks:

    packet = []
    capture = []

    def __init__(self, cmd1, cmd2, data=None):

        match cmd1:
            case commandTypes.CMD1.SystemCommand.value:
                pass
            case commandTypes.CMD1.ImmediateCommand.value:
                pass
            case commandTypes.CMD1.SelectCommand.value:
                pass
            case commandTypes.CMD1.SenseRequest.value:
                match cmd2:
                    case commandTypes.SenseRequestCommands.open_port.value:
                        CommandBlocks.open_port(self)
                    case commandTypes.SenseRequestCommands.next_ten_ids.value:
                        pass
                    case commandTypes.SenseRequestCommands.last_response.value:
                        pass
                    case commandTypes.SenseRequestCommands.port_status.value:
                        CommandBlocks.get_port_status(self)
                    case commandTypes.SenseRequestCommands.position_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.active_id_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.device_type_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.system_status_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.id_list.value:
                        pass
                    case commandTypes.SenseRequestCommands.id_size_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.list_ids_added_to_archive.value:
                        pass
                    case commandTypes.SenseRequestCommands.id_request.value:
                        pass
                    case commandTypes.SenseRequestCommands.request_compression_settings.value:
                        pass
                    case commandTypes.SenseRequestCommands.ids_added_list.value:
                        pass
                    case commandTypes.SenseRequestCommands.ids_deleted_list.value:
                        pass
                    case commandTypes.SenseRequestCommands.multiple_ports_status.value:
                        pass
            case commandTypes.CMD1.TimelineCommand.value:
                pass
            case commandTypes.CMD1.MacroCommand.value:
                pass

    def open_port(self, port_number=0x01, target_port=main.com.port, is_locked=False):

        if is_locked:
            is_locked = 0x01
        else:
            is_locked = 0x00

        self.packet = encoder.encode_packet(
            encoder.encode_commands(
                commandTypes.CMD1.SenseRequest.value,
                commandTypes.SenseRequestCommands.open_port.value,
                [port_number, is_locked]
            )
        )

        target_port.write(self.packet)
        self.capture = target_port.read(50)
        print(self.capture)
        self.capture = binascii.b2a_hex(self.capture)
        print(self.capture)

    def get_port_status(self, target_port="COM1", data=[0, 0, 0, 1, 1, 1, 1, 1]):

        self.packet = encoder.encode_packet(
            encoder.encode_commands(
                commandTypes.CMD1.SenseRequest.value,
                commandTypes.SenseRequestCommands.port_status.value,
                data
            )
        )

        target_port.write(self.packet)
        self.capture = target_port.read(100)
        port_status_decoder = Decoder(self.capture, self.packet)

