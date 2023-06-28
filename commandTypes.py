from enum import Enum


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

