from configparser import ConfigParser

from piradio.stations import Station
from piradio.utils import clamp


class Settings:
    """
    The application settings.
    """

    DEFAULT_VOLUME = 128
    DEFAULT_STATION = 0
    DEFAULT_STATIONS = [Station('ByteFM', 'http://www.byte.fm/stream/bytefm.m3u')]

    def __init__(self, volume, station, stations):
        self.volume = volume
        self.station = station  # selected station index
        self.stations = stations

    @staticmethod
    def get_parser():
        parser = ConfigParser()
        parser.optionxform = str  # case sensitive keys
        return parser

    @classmethod
    def read(cls, file_path):
        parser = cls.get_parser()
        parser.read(file_path)

        config_sec = parser['config']
        volume = config_sec.getint('volume', cls.DEFAULT_VOLUME)
        station = config_sec.getint('station', cls.DEFAULT_STATION)

        stations_sec = parser['stations']
        stations = [
            Station(name=key, url=stations_sec[key])
            for key in stations_sec
        ] or cls.DEFAULT_STATIONS
        station = clamp(0, station, len(stations) - 1)

        return cls(volume, station, stations)

    def save(self, file_path):
        parser = self.get_parser()

        config_sec = parser['config']
        config_sec['volume'] = self.volume
        config_sec['station'] = self.station

        stations_sec = parser['stations']
        for station in self.stations:
            stations_sec[station.name] = station.url

        with open(file_path, 'w') as f:
            parser.write(f)
