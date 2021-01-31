import re
from collections import namedtuple


Station = namedtuple('Station', 'name url')


class Stations:
    """
    A factory class for radio stations.
    """

    RX_STATION = re.compile(r'^\s*(?P<name>[^\s]+)\s+(?P<url>[^\s]+)\s*$')

    @classmethod
    def from_file(cls, file_path):
        """
        Reads text files in the following format and creates a list of
        `Station` instances from it:

        ```
        FooFM      https://www.example.com/live/foo-fm
        SomeRadio! http://www.example.com/stream/some-radio
        ```
        """

        with open(file_path, 'r') as f:
            matches = filter(None, [cls.RX_STATION.match(l) for l in f.readlines()])

        return [Station(m.group('name'), m.group('url')) for m in matches]
