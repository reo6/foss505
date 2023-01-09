"""
Representing a single "Loop".
"""
import numpy as np
import numpy.typing as npt
from enum import Enum
from typing import Any

get_empty_block = lambda bufsize: np.zeros(bufsize, dtype=np.float32)
Block = Any # TODO: np.array[np.float32]
BlockPair = tuple[Block, Block]
Take = list[BlockPair]
LoopMode = Enum("LoopMode", ["PLAY", "RECORD", "OVERDUB"])


class Loop:
    def __init__(self,
                 id: int,
                 bufsize: int,
                 initial_take: Take=[],
                 initial_mode: LoopMode=LoopMode.PLAY):
        self.take = initial_take
        self.mode = initial_mode
        self.__index = 0

    @property
    def index(self):
        """
        Holds the index of the loop.
        """
        return self.__index

    @index.setter
    def index(self, new_value):
        """
        Set new index if the new value covers the take. Otherwise move index to zero.
        """
        if new_value >= len(self.take):
            self.__index = 0
        else:
            self.__index = new_value

    def next_blocks(self) -> BlockPair:
        if len(self.take) == 0:
            return get_empty_block(self.bufsize)

        pair = self.take[self.index]
        self.index += 1

        return pair

    def write_blocks(self, pair: BlockPair):
        """
        Writes the given pair to the current index of the take.
        Extends the take if in the recording mode, doesn't extend if
        overdubbing.
        """
        if self.mode == LoopMode.RECORD:
            self.take.append(pair)
        elif self.mode == LoopMode.OVERDUB:
            self.take[self.index] = pair
            self.index += 1
        elif self.mode == LoopMode.PLAY:
            raise Exception("Cannot write blocks while in play mode.")
