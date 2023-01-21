"""
Representing a single "Loop".
"""
import numpy as np
from enum import Enum
from typing import Any
from foss505.observable import Observable


Block = Any # TODO: np.array[np.float32]
BlockPair = tuple[Block, Block]
Take = list[BlockPair]
LoopMode = Enum("LoopMode", ["PLAY", "RECORD", "OVERDUB", "MUTED", "EMPTY"])


class Loop:
    def __init__(self,
                 id: int,
                 bufsize: int,
                 initial_take: Take=[],
                 initial_mode: LoopMode=LoopMode.EMPTY):
        self.take = initial_take
        self.mode = Observable(initial_mode)
        self.__index = 0
        self.bufsize = bufsize
        self.id = id
        self.is_active = True
        self.gain = 1.0

        self.reset_loop() # See Todo.org/Bugs
        self.reset_loop()

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
            assert self.mode.value.value == LoopMode.EMPTY
            raise Exception("Take is empty.")

        pair = self.take[self.index]
        self.index += 1

        return self.apply_gain(pair)

    def apply_gain(self, pair: BlockPair):
        """
        Apply volume parameter to the given block pair.
        """
        return tuple(map(
            lambda block: np.multiply(block, self.gain), # FIXME
            pair
        ))

    def write_blocks(self, pair: BlockPair) -> BlockPair:
        """
        Writes the given pair to the current index of the take.
        Extends the take if in the recording mode, doesn't extend if
        overdubbing.
        """
        if self.mode.value == LoopMode.RECORD:
            self.take.append(pair)
            return self.apply_gain(pair)
        elif self.mode.value == LoopMode.OVERDUB:
            take_pair = self.take[self.index]
            new_pair = (take_pair[0] + pair[0], take_pair[1] + pair[1])
            self.take[self.index] = new_pair
            self.index += 1
            return self.apply_gain(new_pair)
        elif self.mode.value == LoopMode.PLAY:
            raise Exception("Cannot write blocks while in play mode.")

    def get_name(self):
        return f"Loop Channel #{self.id}"

    def reset_loop(self):
        self.mode.value = LoopMode.EMPTY
        self.take = []
        self.index = 0

    def toggle(self):
        """
        Toggle the looper.
        """
        if self.mode.value == LoopMode.RECORD or self.mode.value == LoopMode.OVERDUB:
            self.mode.value = LoopMode.PLAY

        elif self.mode.value == LoopMode.EMPTY:
            # It's the first toggle.
            self.mode.value = LoopMode.RECORD
        elif self.mode.value == LoopMode.PLAY:
            self.mode.value = LoopMode.OVERDUB
        elif self.mode.value == LoopMode.MUTED:
            self.mode.value = LoopMode.PLAY

    def toggle_mute(self):
        if self.mode.value != LoopMode.MUTED and self.mode.value != LoopMode.PLAY:
            raise Exception("Cannot switch to muted mode when it's not in the play mode.")

        if self.mode.value == LoopMode.MUTED:
            self.mode.value = LoopMode.PLAY
        else:
            self.mode.value = LoopMode.MUTED
