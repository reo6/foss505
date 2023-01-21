from foss505.loop import Loop, LoopMode, Block
import numpy as np
import copy


LOOP_CHANNEL_SIZE = 5
get_empty_block = lambda bufsize: np.zeros(bufsize, dtype=np.float32)
get_empty_pair  = lambda bufsize: (get_empty_block(bufsize), get_empty_block(bufsize))

class Station:
    """
    Holds loop channels.
    """
    def __init__(self,
                 bufsize: int,
                 loop_channel_size: int=LOOP_CHANNEL_SIZE):
        self.bufsize = bufsize
        self.loop_channels = [Loop(n, bufsize) for n in range(1, loop_channel_size+1)]

    def process(self, buffers_l: list[Block], buffers_r: list[Block]) -> tuple[Block, Block]:
        _empty_block = np.zeros(self.bufsize, dtype=np.float32)
        output_l = copy.deepcopy(_empty_block)
        output_r = copy.deepcopy(_empty_block)

        for input_l, input_r, loop in zip(buffers_l, buffers_r, self.loop_channels):
            if loop.mode.value == LoopMode.PLAY:
                """
                Play loop takes and incoming audio together.
                """
                take_l, take_r = loop.next_blocks()
                output_l += take_l + input_l
                output_r += take_r + input_r

            elif loop.mode.value == LoopMode.EMPTY:
                """
                There's nothing recorded. Play incoming audio.
                """
                output_l += input_l
                output_r += input_r

            elif loop.mode.value == LoopMode.MUTED:
                """
                Recorded take (either it exists or not) is muted. Don't play anything.
                Get the next audio blocks to keep the index though.
                """
                _ = loop.next_blocks()
                output_l += get_empty_block(self.bufsize)
                output_r += get_empty_block(self.bufsize)

            elif loop.mode.value == LoopMode.RECORD:
                """
                There should be nothing in the take right now. So play
                incoming audio and also record it.
                """
                loop.write_blocks((input_l, input_r))
                output_l += input_l
                output_r += input_r

            elif loop.mode.value == LoopMode.OVERDUB:
                """
                Overdubbing. Write incoming audio to the loop take,
                and then play the take that is already mixed with the input.
                """
                take_l, take_r = loop.write_blocks((input_l, input_r))
                output_l += take_l
                output_r += take_r

            else:
                print("wtf")

        return (output_l, output_r)
