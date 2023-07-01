import serial
from bitstring import Bits, BitArray, BitStream, pack
import logging
from enum import Enum

logging.basicConfig(filename="python_serial_testing.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())


def check_bit(response_number, bit_place):

    if int(response_number, 16) & (1 << bit_place):
        return True
    else:
        return False


class VDCP:

    packet = []
    capture = []
    serial_port = None

    def send_to_decoder(self):

        self.serial_port.write(self.packet)
        self.capture = self.serial_port.read(50)
        return Decoder(self.capture, self.packet)

    def init_serial(self, com_port="COM1", serial_timeout=2):

        self.serial_port = serial.Serial(com_port)
        self.serial_port.baudrate = 38400
        self.serial_port.parity = serial.PARITY_ODD
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.timeout = serial_timeout

    # --------------------> System Commands

    def local_disable(self):

        # -Opt
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SystemCommand.value,
            CommandTypes.SystemCommands.local_disable.value
        )

        return VDCP.send_to_decoder(self)

    def local_enable(self):

        # -Opt
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SystemCommand.value,
            CommandTypes.SystemCommands.local_enable.value
        )

        return VDCP.send_to_decoder(self)

    @staticmethod
    def delete_from_archive():

        # +Opt
        logging.info("The delete_from_archive function has not been "
                     "implemented as there is no archival system connected "
                     "to this deck - command ignored")

    @staticmethod
    def delete_protect_id():

        # Todo: Implement delete_protect_id
        # +Opt
        logging.info("The function to protect and unprotect clips has not yet been implemented "
                     "but it is planned for the future - command ignored")

    @staticmethod
    def undelete_protect_id():

        # Todo: Implement undelete_protect_id
        # +Opt
        logging.info("The function to protect and unprotect clips has not yet been implemented "
                     "but it is planned for the future - command ignored")

    # --------------------> Immediate Commands

    def stop_port(self):

        # -Req
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.ImmediateCommand.value,
            CommandTypes.ImmediateCommands.stop.value
            )

        return VDCP.send_to_decoder(self)

    def play_port(self, data=None):

        # -Req
        # Todo: Implement data entry to play_port command (see VDCP manual p.20 under 1X.01: PLAY)
        if data:
            logging.info("The function to play a prepared file handle by including "
                         "data in the play_port command has not yet been implemented "
                         "but it is planned for the future - command ignored")
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.ImmediateCommand.value,
            CommandTypes.ImmediateCommands.playID.value
        )

        return VDCP.send_to_decoder(self)

    def record_port(self):

        # -Req
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.ImmediateCommand.value,
            CommandTypes.ImmediateCommands.record.value
        )

        return VDCP.send_to_decoder(self)

    @staticmethod
    def freeze_port():

        # Todo: Implement freeze_port
        # -Opt
        logging.info("The function to freeze input has not yet been implemented "
                     "but it is planned for the future - command ignored")

    def still_port(self):

        # -Opt
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.ImmediateCommand.value,
            CommandTypes.ImmediateCommands.stillID
        )

        return VDCP.send_to_decoder(self)

    def step_port(self):

        # -Opt
        pass

    def continue_port(self):

        # -Opt
        pass

    def jog_port(self):

        # -Opt
        pass

    def vari_play_port(self):

        # -Opt
        pass

    def unfreeze_port(self):

        # -Opt
        pass

    def ee_mode_port(self):

        # -Opt
        pass

    # --------------------> Preset / Select Commands

    def rename_id(self):

        # +Opt
        pass

    def preset_standard_time(self):

        # +Opt
        pass

    def new_copy(self):

        # +Opt
        pass

    def sort_mode(self):

        # +Opt
        pass

    def close_port(self, data=[0x01, ]):

        # -Req
        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SelectCommand.value,
            CommandTypes.SelectCommands.close_port.value,
            data
        )

        return VDCP.send_to_decoder(self)

    def select_port(self, data=[0x01, ]):

        # Req
        self.packet = Encoder.encode_packet(
            Encoder.encode_commands(
                CommandTypes.CMD1.SelectCommand.value,
                CommandTypes.SelectCommands.select_port,
                data
            )
        )

        return VDCP.send_to_decoder(self)

    @staticmethod
    def record_init():

        # -Req
        # Todo: Implement record_init
        logging.info("The function to initialise a record has not yet been implemented "
                     "but it is planned for the future - command ignored")

    def play_cue(self, data=None):

        # -Req
        if not data:
            logging.warning("Please specify a video id to cue up!")

        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SelectCommand.value,
            CommandTypes.SelectCommands.play_cue.value,
            data
        )

        return VDCP.send_to_decoder(self)

    @staticmethod
    def cue_with_data():

        # -Opt
        # Todo: Implement cue_with_data
        pass

    # --------------------> Sense Request Commands

    def open_port(self, port_number=0x01, is_locked=False):

        # -Req
        if is_locked:
            is_locked = 0x01
        else:
            is_locked = 0x00

        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SenseRequest.value,
            CommandTypes.SenseRequestCommands.open_port.value,
            [port_number, is_locked]
            )

        return VDCP.send_to_decoder(self)

    def get_port_status(self, data=BitArray(bin="00011111")):

        self.packet = Encoder.encode_packet(
            Encoder.encode_commands(
                CommandTypes.CMD1.SenseRequest.value,
                CommandTypes.SenseRequestCommands.port_status.value,
                [data.uint, ]
            )
        )

        return VDCP.send_to_decoder(self)

    def active_id_request(self):

        self.packet = Encoder.encode_abstract(
            CommandTypes.CMD1.SenseRequest.value,
            CommandTypes.SenseRequestCommands.active_id_request.value
        )

        return VDCP.send_to_decoder(self)


class Decoder:

    response_list = []
    sent_data = []

    def __init__(self, response, sent_data):

        logging.info("Decoding response")
        logging.info("Converting byte array into hex list")
        self.response_list = [int(byte, 16) for byte in response]

        # ACK
        if response == 0x04:
            logging.info("Command acknowledged by Deck")
        # NAK
        elif self.response_list[0] == 0x05:
            match self.response_list[1], 16:
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
                case CommandTypes.CMD1.SenseRequest.value:
                    self.decode_sense_request(self.response_list, sent_data)
                case CommandTypes.CMD1.TimelineCommand.value:
                    self.decode_timeline_command(self.response_list, self.sent_data)
                case CommandTypes.CMD1.MacroCommand.value:
                    self.decode_macro_command(self.response_list, self.sent_data)
                case _:
                    logging.error(f"Unable to decode response: Bare form - {response}, "
                                  f"Listed form - {self.response_list}")

    def decode_sense_request(self, response_list, sent_data):
        logging.info("Decoding a response to a sense request command")

        match self.response_list[3]:
            case CommandTypes.SenseRequestCommands.response_open_port.value:
                if response_list[4] == 0x1:
                    logging.info("Port Granted")
                    # Todo: set a global variable indicating whether or not there is an open signal port
                elif response_list[4] == 0x0:
                    logging.info("Port Denied")
                else:
                    logging.warning(f"Unexpected response: Listed form - {response_list}")
            case CommandTypes.SenseRequestCommands.response_next_ten_ids.value:
                # Todo: Implement based on data format of LIST command (0x30, 0x11)
                pass
            case CommandTypes.SenseRequestCommands.response_last_response.value:
                logging.info("Last Response has not been implemented")
            case CommandTypes.SenseRequestCommands.response_port_status_request.value:
                # Data format - 0x2, BC, 0x30, 0x85, Data 1 (Port Status Bitmap), Data ...
                decoded_response = StatusCodes(self.response_list)
                decoded_response.log_status_all()
            case CommandTypes.SenseRequestCommands.response_active_id_request.value:
                for i in self.response_list:
                    print(int(i))
            case _:
                logging.info(response_list)

    def decode_timeline_command(self, response_list, sent_data):
        logging.info("Decoding a response to a timeline command")
        logging.warning("Timeline Commands have not been implemented!")
        print(self.response_list)

    def decode_macro_command(self, response_list, sent_data):
        logging.info("Decoding a response to a macro command")
        logging.warning("Macro commands have not been implemented!")
        print(self.response_list)


class CommandTypes:

    class CMD1(Enum):

        SystemCommand = 0x00
        ImmediateCommand = 0x10
        SelectCommand = 0x20
        SenseRequest = 0x30
        TimelineCommand = 0x40
        MacroCommand = 0x50

    class SystemCommands(Enum):

        sys_cmd = 0x00
        local_disable = 0x0C
        local_enable = 0x0D
        delete_from_archive = 0x14
        delete_protect_id = 0x15
        undelete_protect_id = 0x16

    class ImmediateCommands(Enum):

        imm_cmd = 0x10
        stop = 0x00
        playID = 0x01
        record = 0x02
        freeze = 0x03
        stillID = 0x04
        stepID = 0x05
        continueID = 0x06
        jog = 0x07
        variablePlay = 0x08
        unfreeze = 0x09
        eeMode = 0x0A

    class SelectCommands(Enum):

        rename_id = 0x1D
        preset_standard_time = 0x1E
        new_copy = 0x1F
        sort_mode = 0x20
        close_port = 0x21
        select_port = 0x22
        record_init = 0x23
        play_cue = 0x24
        cue_with_data = 0x25
        delete_id = 0x26
        get_from_archive = 0x27
        select_clear = 0x29
        send_to_archive = 0x2A
        percent_to_signal_full = 0x2B
        record_init_with_data = 0x2C
        select_logical_drive = 0x2D
        system_delete_id = 0x2E
        preset = 0x30
        video_compression_rate = 0x31
        audio_sample_rate = 0x32
        audio_compression_rate = 0x33
        audio_in_level = 0x34
        audio_out_level = 0x35
        video_compression_params = 0x37
        select_output = 0x38
        select_input = 0x39
        record_mode = 0x3A
        sc_adjust = 0x41
        horizontal_position_adjust = 0x42
        disk_preroll = 0x43
        copy_file_to = 0x50
        delete_file_from = 0x51
        abort_copy_file = 0x52

    class SenseRequestCommands(Enum):

        open_port = 0x01
        next_ten_ids = 0x02
        last_response = 0x03
        port_status = 0x05
        position_request = 0x06
        active_id_request = 0x07
        device_type_request = 0x08
        system_status_request = 0x10
        id_list = 0x11
        id_size_request = 0x14
        list_ids_added_to_archive = 0x15
        id_request = 0x16
        request_compression_settings = 0x17
        ids_added_list = 0x18
        ids_deleted_list = 0x19
        multiple_ports_status = 0x25

        response_open_port = 0x81
        response_next_ten_ids = 0x82
        response_last_response = 0x83
        response_port_status_request = 0x85
        response_position_request = 0x86
        response_active_id_request = 0x87
        response_device_type_request = 0x88
        response_system_status_request = 0x90
        response_id_list = 0x91
        response_id_size_request = 0x94
        response_list_ids_added_to_archive = 0x95
        response_id_request = 0x96
        response_compression_settings = 0x97
        response_ids_added_list = 0x98
        response_ids_deleted_list = 0x99
        response_miltiple_ports_status = 0xA5


class StatusCodes:

    byte_count = 4

    state_flag_status = False
    port_idle_state = False
    cue_init_state = False
    play_rec_state = False
    still_state = False
    jog_state = False
    vari_play_state = False
    port_busy_state = False
    cue_init_done = False
    port_id = 0x0

    port_hardware_media_status = False
    port_inoperative = False
    new_ids_added = False
    ids_recently_deleted = False
    new_ids_archived = False
    no_input_reference = False
    no_video_input = False
    no_audio_input = False
    audio_beyond_limit = False

    port_error_status = False
    system_error = False
    illegal_value = False
    invalid_port = False
    wrong_port_type = False
    command_queue_full = False
    disk_full = False
    cmd_while_busy = False
    not_supported = False
    invalid_id = False
    id_not_found = False
    id_already_exists = False
    id_still_recording = False
    id_still_playing = False
    id_not_transferred_from_archive = False
    id_not_transferred_to_archive = False
    id_delete_protected = False
    not_in_cue_init_state = False
    cue_not_done = False
    port_not_idle = False
    port_playing_active = False
    port_not_active = False
    cue_or_operation_failed = False
    network_error = False
    system_rebooted = False

    # Port settings not implemented
    port_settings = False
    port_format_off = False
    port_format_composite = False
    port_format_svideo = False
    port_format_yuv = False
    port_format_d1 = False

    # Compression type not implemented
    video_compression_type = False
    video_compression_default = False
    video_compression_jpeg = False
    video_compression_mpeg420 = False
    video_compression_mpeg422 = False
    video_compression_type_4 = False
    video_compression_type_5 = False
    video_compression_type_6 = False
    video_compression_type_7 = False

    def __init__(self, response_list):

        if check_bit(response_list[4], 0):
            self.byte_count += 1
            self.state_flag_status = True
            self.port_idle_state = check_bit(response_list[self.byte_count], 0)
            self.cue_init_state = check_bit(response_list[self.byte_count], 1)
            self.play_rec_state = check_bit(response_list[self.byte_count], 2)
            self.still_state = check_bit(response_list[self.byte_count], 3)
            self.jog_state = check_bit(response_list[self.byte_count], 4)
            self.vari_play_state = check_bit(response_list[self.byte_count], 5)
            self.port_busy_state = check_bit(response_list[self.byte_count], 6)
            self.cue_init_done = check_bit(response_list[self.byte_count], 7)
            self.byte_count += 1
            self.port_id = response_list[self.byte_count]

        if check_bit(response_list[4], 1):
            self.byte_count += 1
            self.port_hardware_media_status = True
            self.port_inoperative = check_bit(response_list[self.byte_count], 0)
            self.new_ids_added = check_bit(response_list[self.byte_count], 1)
            self.ids_recently_deleted = check_bit(response_list[self.byte_count], 2)
            self.new_ids_archived = check_bit(response_list[self.byte_count], 3)
            self.no_input_reference = check_bit(response_list[self.byte_count], 4)
            self.no_video_input = check_bit(response_list[self.byte_count], 5)
            self.no_audio_input = check_bit(response_list[self.byte_count], 6)
            self.audio_beyond_limit = check_bit(response_list[self.byte_count], 7)

        if check_bit(response_list[4], 2):
            self.byte_count += 1
            self.port_error_status = True
            self.system_error = check_bit(response_list[self.byte_count], 0)
            self.illegal_value = check_bit(response_list[self.byte_count], 1)
            self.invalid_port = check_bit(response_list[self.byte_count], 2)
            self.wrong_port_type = check_bit(response_list[self.byte_count], 3)
            self.command_queue_full = check_bit(response_list[self.byte_count], 4)
            self.disk_full = check_bit(response_list[self.byte_count], 5)
            self.cmd_while_busy = check_bit(response_list[self.byte_count], 6)
            self.not_supported = check_bit(response_list[self.byte_count], 7)
            self.byte_count += 1
            self.invalid_id = check_bit(response_list[self.byte_count], 0)
            self.id_not_found = check_bit(response_list[self.byte_count], 1)
            self.id_already_exists = check_bit(response_list[self.byte_count], 2)
            self.id_still_recording = check_bit(response_list[self.byte_count], 3)
            self.id_still_playing = check_bit(response_list[self.byte_count], 4)
            self.id_not_transferred_from_archive = check_bit(response_list[self.byte_count], 5)
            self.id_not_transferred_to_archive = check_bit(response_list[self.byte_count], 6)
            self.id_delete_protected = check_bit(response_list[self.byte_count], 7)
            self.byte_count += 1
            self.not_in_cue_init_state = check_bit(response_list[self.byte_count], 0)
            self.cue_not_done = check_bit(response_list[self.byte_count], 1)
            self.port_not_idle = check_bit(response_list[self.byte_count], 2)
            self.port_playing_active = check_bit(response_list[self.byte_count], 3)
            self.port_not_active = check_bit(response_list[self.byte_count], 4)
            self.cue_or_operation_failed = check_bit(response_list[self.byte_count], 5)
            self.network_error = check_bit(response_list[self.byte_count], 6)
            self.system_rebooted = check_bit(response_list[self.byte_count], 7)

        if check_bit(response_list[4], 3):
            self.byte_count += 1
            self.port_settings = True
            self.port_format_off = check_bit(response_list[self.byte_count], 0)
            self.port_format_composite = check_bit(response_list[self.byte_count], 1)
            self.port_format_svideo = check_bit(response_list[self.byte_count], 2)
            self.port_format_yuv = check_bit(response_list[self.byte_count], 3)
            self.port_format_d1 = check_bit(response_list[self.byte_count], 4)

        if check_bit(response_list[4], 4):
            self.byte_count += 1
            self.video_compression_type = True
            self.video_compression_default = check_bit(response_list[self.byte_count], 0)
            self.video_compression_jpeg = check_bit(response_list[self.byte_count], 1)
            self.video_compression_mpeg420 = check_bit(response_list[self.byte_count], 2)
            self.video_compression_mpeg422 = check_bit(response_list[self.byte_count], 3)
            self.video_compression_type_4 = check_bit(response_list[self.byte_count], 4)
            self.video_compression_type_5 = check_bit(response_list[self.byte_count], 5)
            self.video_compression_type_6 = check_bit(response_list[self.byte_count], 6)
            self.video_compression_type_7 = check_bit(response_list[self.byte_count], 7)

    def log_status_all(self):

        if self.state_flag_status:
            logging.info("\n")
            logging.info("State / Flags Status:\n")

            if self.port_idle_state:
                logging.info("The system is in the IDLE state")
            if self.cue_init_state:
                logging.info("The system is cueing or initialising")
            if self.play_rec_state:
                logging.info("The system is in the PLAY or RECORD state")
            if self.still_state:
                logging.info("The system is in the STILL state")
            if self.still_state:
                logging.info("The system is in the JOG state")
            if self.vari_play_state:
                logging.info("The system is in the VARI PLAY state")
            if self.port_busy_state:
                logging.info("PORT BUSY")
            if self.cue_init_done:
                logging.info("CUE / INIT DONE - System is ready to accept another command")

            logging.info(f"The selected port ID is: {self.port_id}")

        if self.port_hardware_media_status:
            logging.info("\n")
            logging.info("Port Hardware / Media Status:\n")

            if self.port_inoperative:
                logging.warning("PORT INOPERATIVE")
            if self.new_ids_added:
                logging.info("New ID’s have been added to the disk system by recording "
                             "or transferring from an archive system")
            if self.ids_recently_deleted:
                logging.info("ID’s have been deleted from the disk")
            if self.new_ids_archived:
                logging.info("New ID’s have been added to an archive system connected to the disk system")
            if self.no_input_reference:
                logging.info("The system has no input reference")
            if self.no_video_input:
                logging.info("The port has no video input")
            if self.no_audio_input:
                logging.info("The port has no audio input")
            if self.audio_beyond_limit:
                logging.warning("The input audio level is beyond limit")

        if self.port_error_status:
            logging.info("\n")
            logging.info("Port Error Status:\n")

            if self.system_error:
                logging.error("A FUNCTIONAL ERROR HAS BEEN DETECTED")
            if self.illegal_value:
                logging.warning("A command with an invalid value has been given - command ignored")
            if self.invalid_port:
                logging.info("Invalid port - the port ID may be invalid, "
                             "or the port may be unavailable due to being already opened and locked")
            if self.wrong_port_type:
                logging.info("The controlling device has issued a command "
                             "not applicable to the open port - command ignored")
            if self.command_queue_full:
                logging.info("The disk can not process the command because it has too many commands pending")
            if self.disk_full:
                logging.info("Disk full - can't fit any more media")
            if self.cmd_while_busy:
                logging.info("A command, other than an Immediate Command was "
                             "issued while the busy bit was set - command ignored")
            if self.not_supported:
                logging.info("A command was issued that is not supported by the device - command ignored")
            if self.invalid_id:
                logging.info("Invalid ID specified - command ignored")
            if self.id_not_found:
                logging.info("Specified ID was not found - command ignored")
            if self.id_already_exists:
                logging.info("Specified ID already exists - command ignored")
            if self.id_still_recording:
                logging.info("ID is still recording - command ignored")
            if self.id_still_playing:
                logging.info("ID is still playing - command ignored")
            if self.id_not_transferred_from_archive:
                logging.info("ID not yet transferred from archive - command ignored")
            if self.id_not_transferred_to_archive:
                logging.info("ID not yet transferred to archive and already exists on the disk - command ignored")
            if self.id_delete_protected:
                logging.info("ID is delete protected. Can not delete ID - command ignored")
            if self.not_in_cue_init_state:
                logging.info("A command was issued which requires the system to "
                             "be in the cueing state - command ignored")
            if self.cue_not_done:
                logging.info("A command was issued which requires the system to "
                             "be in the cue/init done state - command ignored")
            if self.port_not_idle:
                logging.info("A command was issued which requires the system to "
                             "be in the idle state - command ignored")
            if self.port_playing_active:
                logging.info("A command was issued which requires the system to "
                             "not be in the play state - command ignored")
            if self.port_not_active:
                logging.info("A command was issued which requires the system to "
                             "be playing, recording, or active - command ignored")
            if self.cue_or_operation_failed:
                logging.error("A CUE command or other command that has been ACKed "
                              "and started has failed for some unknown reason - command "
                              "will not be executed correctly")
            if self.network_error:
                logging.info("File transfer cancelled due to network error")
            if self.system_rebooted:
                logging.info("System has been rebooted. Controller must do PORT OPEN "
                             "and SELECT commands, plus any other start up command sequence")


class Encoder:

    @staticmethod
    def encode_commands(command_1, command_2, data=None):

        packet_content = bytearray()

        packet_content.append(command_1)
        packet_content.append(command_2)

        if data:
            for bit in data:
                packet_content.append(bit)

        return packet_content

    @staticmethod
    def get_checksum(packet_content):

        data_sum = 0

        for data in packet_content:
            data_sum += data

        data_sum = -(data_sum % 256)

        return '%2X' % (data_sum & 0xFF)

    @staticmethod
    def encode_packet(packet_content):

        packet = bytearray()
        bit_count = len(packet_content)
        checksum_value = int(Encoder.get_checksum(packet_content), 16)

        packet.append(0x02)
        packet.append(bit_count)
        packet = packet + packet_content
        packet.append(checksum_value)

        return packet

    @staticmethod
    def encode_abstract(encoder_cmd1, encoder_cmd2, data=None):

        return Encoder.encode_commands(
            encoder_cmd1,
            encoder_cmd2,
            data
        )
