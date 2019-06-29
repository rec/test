from enum import IntEnum

class RETURN_CODES(IntEnum):
    SUCCESS = 255  # All is well
    REBOOT = 42  # Device reboot needed after configuration
    ERROR = 0  # Generic error
    ERROR_SIZE = 1  # Data receieved does not match given command length
    ERROR_UNSUPPORTED = 2  # Unsupported command
    ERROR_PIXEL_COUNT = 3  # Too many pixels for device
    ERROR_BAD_CMD = 4  # Unknown Command
    NONE = 512  # The device did not respond
    EMPTY = 1024  # The device responded with an empty packet
