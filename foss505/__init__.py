from foss505.jackclient import JackClient
from foss505.loop import LoopMode
from foss505.ui import run_ui


def run():
    client = JackClient()
    with client.client:
        capture = client.client.get_ports(is_physical=True, is_input=True)
        for src, dest in zip(client.client.outports, capture):
            client.client.connect(src, dest)

        run_ui(client.station)
