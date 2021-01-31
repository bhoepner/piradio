#!/usr/bin/env python3

from signal import SIGINT, SIGTERM, signal
from time import sleep

from piradio.rotary import RotaryEncoder
from piradio.settings import Settings
from piradio.vlc import VlcRemote


class Runner:
    MODE_VOLUME = 0
    MODE_STATIONS = 1

    def __init__(self):
        self._vlc = VlcRemote()
        self._rot = RotaryEncoder()
        self._mode = self.MODE_VOLUME
        self._station = None

    def run(self):
        self._initialize()

        prev_title = None
        prev_playing = None

        while True:
            title = self._vlc.get_title()
            playing = self._vlc.get_playing()

            if title != prev_title:
                print(title or '')
                prev_title = title

            if playing != prev_playing:
                print(playing or '')
                prev_playing = playing

            sleep(0.5)

    def _initialize(self):
        settings = Settings.read('settings.ini')
        self._vlc.connect()
        self._vlc.stop()
        self._vlc.clear()
        for station in settings.stations:
            self._vlc.enqueue(station.url)

        self._vlc.set_volume(settings.volume)
        self._vlc.play()
        for _ in range(settings.station):
            self._vlc.next()

        self._station = settings.station

        self._rot.setup()
        self._rot.on_rotate(self._on_rotate)
        self._rot.on_switch(self._on_switch)

        signal(SIGINT, self._on_signal)
        signal(SIGTERM, self._on_signal)

    def _shutdown(self):
        self._rot.off_rotate()
        self._rot.off_switch()
        self._rot.shutdown()
        self._vlc.stop()
        self._vlc.disconnect()

    def _on_signal(self, sig, frame):
        self._shutdown()

    def _on_rotate(self, direction):
        print('rotation:', direction)
        if direction == RotaryEncoder.CLOCKWISE:
            if self._mode == self.MODE_VOLUME:
                self._vlc.volume_up()
            else:
                self._vlc.next()

        if direction == RotaryEncoder.COUNTERCLOCKWISE:
            if self._mode == self.MODE_VOLUME:
                self._vlc.volume_down()
            else:
                self._vlc.prev()

    def _on_switch(self):
        print('switch')
        self._mode = (
            self.MODE_STATIONS
            if self._mode == self.MODE_VOLUME
            else self.MODE_VOLUME
        )


if __name__ == '__main__':
    runner = Runner()
    runner.run()
