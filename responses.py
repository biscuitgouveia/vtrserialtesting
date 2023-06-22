from enum import Enum


class PortStatus(Enum):

    port_status_1 = 0x02
    port_status_2 = 0x04
    port_status_3 = 0x04
    port_status_4 = 0x08
    port_status_5 = 0x10


class PortStatus1(Enum):

    idle_state = 0x01
    cue_init_state = 0x02
    play_rec_state = 0x04
    still_state = 0x08
    jog_state = 0x10
    var_play_state = 0x12
    port_busy_state = 0x20
