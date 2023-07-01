import logging
import commandTypes
from statusCodes import StatusCodes

logging.basicConfig(filename="python_serial_testing.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())


def check_bit(response_number, bit_place):

    if response_number & (1 << bit_place):
        return True
    else:
        return False


class Decoder:

    response_list = []
    sent_data = []

    def __init__(self, response, sent_data):

        logging.info("Decoding response")
        logging.info("Converting byte array into hex list")
        self.response_list = [hex(byte) for byte in response]

        # ACK
        if response == 0x04:
            logging.info("Command acknowledged by Deck")
        # NAK
        elif self.response_list[0] == 0x05:
            match self.response_list[1]:
                case 0x01:
                    logging.warning("Undefined Error:\nThe command received could not be interpreted "
                                    "as one from this protocol.\n***Command ignored***")
                case 0x04:
                    logging.warning("Checksum Error:\nThe checksum of the data received "
                                    "(as calculated by the disk system per this protocol) does not "
                                    "match the checksum that was sent in the last byte of the command\n"
                                    "***Command Ignored***")
                case 0x10:
                    logging.error("Parity Error")
                case 0x20:
                    logging.error("Overrun Error")
                case 0x40:
                    logging.error("Framing Error")
                case 0x80:
                    logging.warning("Time Out:\nMore than 10 milliseconds have past since last byte "
                                    "was received and the number of bytes required by the byte count "
                                    "has not been received\n***Disk system has flushed the input buffer***\n"
                                    "***System awaits next message***")
                case _:
                    logging.error(f"Unable to parse error bytes:\nBare form - {response}\n"
                                  f"Listed form - {self.response_list}")
        else:
            match self.response_list[2]:
                case int(commandTypes.CMD1.SenseRequest.value, 16):
                    self.decode_sense_request(self.response_list, sent_data)
                case int(commandTypes.CMD1.TimelineCommand.value, 16):
                    self.decode_timeline_command(self.response_list, self.sent_data)
                case int(commandTypes.CMD1.MacroCommand.value, 16):
                    self.decode_macro_command(self.response_list, self.sent_data)
                case _:
                    logging.error(f"Unable to decode response: Bare form - {response}, "
                                  f"Listed form - {self.response_list}")

    def decode_sense_request(self, response_list, sent_data):
        logging.info("Decoding a response to a sense request command")

        match self.response_list[3]:
            case commandTypes.SenseRequestCommands.response_open_port.value:
                if response_list[4] == 0x1:
                    logging.info("Port Granted")
                    # Todo: set a global variable indicating whether or not there is an open signal port
                elif response_list[4] == 0x0:
                    logging.info("Port Denied")
                else:
                    logging.warning(f"Unexpected response: Listed form - {response_list}")
            case commandTypes.SenseRequestCommands.response_next_ten_ids.value:
                # Todo: Implement based on data format of LIST command (0x30, 0x11)
                pass
            case commandTypes.SenseRequestCommands.response_last_response.value:
                logging.info("Last Response has not been implemented")
            case commandTypes.SenseRequestCommands.response_port_status_request.value:
                # Data format - 0x2, BC, 0x30, 0x85, Data 1 (Port Status Bitmap), Data ...
                decoded_response = StatusCodes(self.response_list)

    def decode_timeline_command(self, response_list, sent_data):
        logging.info("Decoding a response to a timeline command")
        logging.warning("Timeline Commands have not been implemented!")
        print(self.response_list)

    def decode_macro_command(self, response_list, sent_data):
        logging.info("Decoding a response to a macro command")
        logging.warning("Macro commands have not been implemented!")
        print(self.response_list)
