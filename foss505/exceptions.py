class MuteError(Exception):
    """
    Something unexpected happened at the mute process.
    """

class ToggleError(Exception):
    """
    Something unexpected happened at the toggling process.
    """

class EmptyTakeError(Exception):
    """
    Next block is requested while there's nothing in the take.
    """

class BlockWriteError(Exception):
    """
    Cannot write blocks.
    """
