import logging
import commandTypes

logging.basicConfig(filename="python_serial_testing.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())


def check_bit(response_number, bit_place):

    if response_number & (1 << bit_place):
        return True
    else:
        return False


def decode_response(response, sent_data):

    logging.info("Decoding response")
    logging.info("Converting byte array into hex list")
    response_list = [hex(byte) for byte in response]

    # ACK
    if response == 0x04:
        logging.info("Command acknowledged by Deck")
    # NAK
    elif response_list[0] == 0x05:
        match response[1]:
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
                logging.error(f"Unable to parse error bytes:\nBare form - {response}\nListed form - {response_list}")
    else:
        match response_list[2]:
            case commandTypes.CMD1.SenseRequest.value:
                return decode_sense_request(response_list, sent_data)
            case commandTypes.CMD1.TimelineCommand.value:
                return decode_timeline_command(response_list, sent_data)
            case commandTypes.CMD1.MacroCommand.value:
                return decode_macro_command(response_list, sent_data)
            case _:
                logging.error(f"Unable to decode response: Bare form - {response}, Listed form - {response_list}")


def decode_sense_request(response_list, sent_data):
    logging.info("Decoding a response to a sense request command")

    match response_list[3]:
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

            byte_count = 4

            if check_bit(response_list[4], 0):
                byte_count += 1
                state_flag_status = True
                logging.info("State and Flag Status:")
                logging.info(f"Port Idle: {check_bit(response_list[byte_count], 0)}")
                logging.info(f"Cue/Init State: {check_bit(response_list[byte_count], 1)}")
                logging.info(f"Play/Record State: {check_bit(response_list[byte_count], 2)}")
                logging.info(f"Still State: {check_bit(response_list[byte_count], 3)}")
                logging.info(f"Jog State: {check_bit(response_list[byte_count], 4)}")
                logging.info(f"Variable Play State: {check_bit(response_list[byte_count], 5)}")
                logging.info(f"Port Busy State: {check_bit(response_list[byte_count], 6)}")
                logging.info(f"Cue/Init Done: {check_bit(response_list[byte_count], 7)}")
                byte_count += 1
                logging.info(f"Port ID: {response_list[byte_count]}")

            if check_bit(response_list[4], 1):
                byte_count += 1
                logging.info("Port Hardware/Media Status:")
                logging.info(f"Port Inoperative: {check_bit(response_list[byte_count], 0)}")
                logging.info(f"New IDs have been added: {check_bit(response_list[byte_count], 1)}")
                logging.info(f"IDs have been deleted: {check_bit(response_list[byte_count], 2)}")
                logging.info(f"New IDs have been added to archive system: {check_bit(response_list[byte_count], 3)}")
                logging.info(f"System has no input reference: {check_bit(response_list[byte_count], 4)}")
                logging.info(f"Port has no video input: {check_bit(response_list[byte_count], 5)}")
                logging.info(f"Port has no audio input: {check_bit(response_list[byte_count], 6)}")
                logging.info(f"Audio input level is beyond limit: {check_bit(response_list[byte_count], 7)}")

            if check_bit(response_list[4], 2):
                byte_count += 1
                logging.info("Port Error Status:")
                logging.info(f"Functional Error Detected: {check_bit(response_list[byte_count], 0)}")
                logging.info(f"System has received an illegal value: {check_bit(response_list[byte_count], 1)}")
                logging.info(f"Selected port either : {check_bit(response_list[byte_count], 2)}")
                logging.info(f"New IDs have been added to archive system: {check_bit(response_list[byte_count], 3)}")
                logging.info(f"System has no input reference: {check_bit(response_list[byte_count], 4)}")
                logging.info(f"Port has no video input: {check_bit(response_list[byte_count], 5)}")
                logging.info(f"Port has no audio input: {check_bit(response_list[byte_count], 6)}")
                logging.info(f"Audio input level is beyond limit: {check_bit(response_list[byte_count], 7)}")



def decode_timeline_command(response_list, sent_data):
    logging.info("Decoding a response to a timeline command")
    logging.warning("Timeline Commands have not been implemented!")


def decode_macro_command(response_list, sent_data):
    logging.info("Decoding a response to a macro command")
    logging.warning("Macro commands have not been implemented!")
