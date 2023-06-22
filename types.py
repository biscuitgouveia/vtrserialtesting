from enum import Enum


class CMD1(Enum):

    SystemCommand = 0x00
    ImmediateCommand = 0x10
    SelectCommand = 0x20
    SenseRequest = 0x30
    TimelineCommand = 0x40
    MacroCommand = 0x50


class SystemCommands(Enum):

    LocalDisable = 0x0C
    LocalEnable = 0x0D
    DeleteProtectID = 0x15
    UnDeleteProtectID = 0x16


class ImmediateCommands(Enum):

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
