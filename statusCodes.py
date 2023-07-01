import logging

logging.basicConfig(filename="python_serial_testing.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())


def check_bit(response_number, bit_place):

    if int(response_number, 16) & (1 << bit_place):
        return True
    else:
        return False


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
