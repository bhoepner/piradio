from piradio.vlc import VLCD_HOST, VLCD_PORT, VlcRemote


class EventLoop:
    """
    The PiRadio's main loop.

    Performs VLCD interaction, button input handling, and rendering.
    Implements a context manager.
    """

    def __init__(self, stations, host=VLCD_HOST, port=VLCD_PORT):
        self._stations = stations
        self._vlc = VlcRemote(host, port)

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False

    def initialize(self):
        self._vlc.connect()

    def shutdown(self):
        self._vlc.disconnect()

    def update(self, deltatime):
        pass

    def render(self):
        pass
