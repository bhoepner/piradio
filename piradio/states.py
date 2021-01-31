import time
from datetime import datetime


class State:
    """
    The base class for all states the PiRadio can be in.

    Think of a finite state machine.
    """

    def start(self):
        """
        Initialize the state.
        """
        pass

    def update(self, deltatime):
        """
        Update the state's internals, based on the passed time.

        Heavy lifting is done here.
        """
        pass

    def render(self):
        """
        Draw the state.

        This should be a fast and straight-forward operation.
        """
        pass

    def sleep(self):
        """
        Make the state sleep.

        This is used to hand over cycle time to the operating system, giving it
        time to breath. This allows other processes to operate in the meantime.

        The sleep time can be varied based on the demands of the state. Fluid
        animations will require shorter cycle times, while displaying a clock
        could e.g. be updated just once a second.
        """
        time.sleep(0.2)

    def stop(self):
        """
        Shut down the state.
        """
        pass


class ClockState(State):
    """
    The state displaying the current time.
    """

    def __init__(self):
        self._timer = 0.0
        self._hour = 0
        self._minute = 0
        self._show_colon = False

    def start(self):
        self._timer = 0.0

    def update(self, deltatime):
        time = datetime.now().time()
        self._timer += (self._timer + deltatime) % 2  # crop to two seconds
        self._hour = time.hour
        self._minute = time.minute
        self._show_colon = self._timer < 1  # show colon in first second of two

    def render(self):
        time_str = ''.join([
            '{:.2f}'.format(self._hour),
            ':' if self._show_colon else ' ',
            '{:.2f}'.format(self._minute),
        ])
        print(time_str)
