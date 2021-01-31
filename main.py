#!/usr/bin/env python3
import time

from piradio.settings import Settings
from piradio.vlc import VlcRemote


if __name__ == '__main__':
    settings = Settings.read('settings.ini')

    vlc = VlcRemote()
    with VlcRemote() as vlc:
        print(vlc.version)
        vlc.stop()

        vlc.clear()
        for station in settings.stations:
            vlc.enqueue(station.url)

        vlc.set_volume(settings.volume)
        vlc.play()
        for _ in range(settings.station):
            vlc.next()

        print(f'playlist:\n{vlc.get_playlist()}')
        time.sleep(1)

        print(f'title:   {vlc.get_title()}')
        print(f'playing: {vlc.get_playing()}')
