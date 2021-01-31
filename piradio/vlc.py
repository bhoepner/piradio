import re
import socket
import sys

from piradio.utils import clamp


VLCD_HOST = '127.0.0.1'
VLCD_PORT = 7070


class VlcRemote:
    """
    The remote control for the VLC daemon.

    Uses a socket connection to communicate with the VLC daemon, which needs
    to run in `-I rc` mode.

    This class imlements a context manager, so it can be used in a `with`
    statement: The socket connection is opened on enter, and closed on exit.
    """

    MIN_VOLUME = 0
    MAX_VOLUME = 512

    BUF_SIZE = 16 * 1024

    CMD_CLEAR = b'clear'
    CMD_ENQUEUE = b'enqueue'
    CMD_STOP = b'stop'
    CMD_PLAY = b'play'
    CMD_NEXT = b'next'
    CMD_PREV = b'prev'
    CMD_VOLUP = b'volup'
    CMD_VOLDOWN = b'voldown'
    CMD_VOLUME = b'volume'
    CMD_PLAYLIST = b'playlist'
    CMD_INFO = b'info'

    RX_PROMPT = re.compile(r'(?:^|\r\n)> $')
    RX_VERSION = re.compile(r'^([^\r\n]+)')
    RX_TITLE = re.compile(r'^\| title: ([^\r\n]+)', re.MULTILINE)
    RX_PLAYING = re.compile(r'^\| now_playing: ([^\r\n]+)', re.MULTILINE)

    def __init__(self, host=VLCD_HOST, port=VLCD_PORT):
        self._host = host
        self._port = port
        self._encoding = sys.getdefaultencoding()
        self._socket = None
        self._version = None

    @property
    def version(self):
        return self._version

    def connect(self):
        self.disconnect()
        self._socket = socket.create_connection((self._host, self._port))
        match = self.RX_VERSION.search(self._execute())
        self._version = match.group(1) if match else None

    def disconnect(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    def clear(self):
        self._execute(self.CMD_CLEAR)

    def enqueue(self, uri):
        self._execute(self.CMD_ENQUEUE, uri.encode(self._encoding))

    def stop(self):
        self._execute(self.CMD_STOP)

    def play(self):
        self._execute(self.CMD_PLAY)

    def next(self):
        self._execute(self.CMD_NEXT)

    def prev(self):
        self._execute(self.CMD_PREV)

    def volume_up(self):
        self._execute(self.CMD_VOLUP)

    def volume_down(self):
        self._execute(self.CMD_VOLDOWN)

    def get_volume(self):
        try:
            return int(self._execute(self.CMD_VOLUME))
        except ValueError:
            return None

    def set_volume(self, volume):
        volume = clamp(self.MIN_VOLUME, volume, self.MAX_VOLUME)
        self._execute(self.CMD_VOLUME, str(volume).encode(self._encoding))

    def get_playlist(self):
        return self._execute(self.CMD_PLAYLIST)

    def get_title(self):
        return self._search_info(self.RX_TITLE)

    def get_playing(self):
        return self._search_info(self.RX_PLAYING)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

    def _search_info(self, rx_pattern):
        info = self._execute(self.CMD_INFO)
        match = rx_pattern.search(info)
        return match.group(1) if match else None

    def _execute(self, command=None, *args):
        if command:
            self._send(command, *args)

        # collect VLC output until prompt
        output = self._receive()
        while not self.RX_PROMPT.search(output):
            output += self._receive()

        # drop the prompt
        return output[:-2]

    def _send(self, command, *args):
        assert self._socket
        command = b' '.join([command, *args]) + b'\r\n'
        self._socket.send(command)

    def _receive(self):
        assert self._socket
        return self._socket.recv(self.BUF_SIZE).decode(self._encoding)
