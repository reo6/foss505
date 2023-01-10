"""
Everything related to Jack.
"""
import jack
from foss505.loop import Loop
from foss505.station import Station, LOOP_CHANNEL_SIZE
import copy
CLIENT_NAME = "Foss505"


class JackClient:
    def __init__(self, client_name: str=CLIENT_NAME):
        self.client = jack.Client(client_name)
        self.station = Station(self.client.blocksize)

        self.initialize_ports()
        self.client.set_process_callback(self.process)

    def initialize_ports(self):
        looper_in_prefix = "looper{n}_in_{s}"

        self.looper_inputs_left = [
            self.client.inports.register(looper_in_prefix.format(n=loop.id, s="l"))
            for loop in self.station.loop_channels
        ]

        self.looper_inputs_right = [
            self.client.inports.register(looper_in_prefix.format(n=loop.id, s="r"))
            for loop in self.station.loop_channels
        ]

        self.output_ports = [
            self.client.outports.register("output_l"),
            self.client.outports.register("output_r"),
        ]

    def process(self, nframes):
        looper_buffers_left = [
            copy.deepcopy(port.get_array())
            for port in self.looper_inputs_left
        ]

        looper_buffers_right = [
            copy.deepcopy(port.get_array())
            for port in self.looper_inputs_right
        ]

        loop_output = self.station.process(
            looper_buffers_left,
            looper_buffers_right,
        )

        for outport, loop_out in zip(self.output_ports, loop_output):
            outport.get_buffer()[:] = loop_out
