"""
A module taking care of the rotary encoder.
"""

from RPi import GPIO


PIN_A = 27
PIN_B = 22
PIN_SWITCH = 25


class RotaryEncoder:

    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1
    UNDECIDED = 0

    STEPS = (
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 0),
    )

    def __init__(self, a=PIN_A, b=PIN_B, switch=PIN_SWITCH):
        self._a = a
        self._b = b
        self._switch = switch
        self._is_setup = False
        self._step = self.STEPS[0]
        self._moved = 0
        self._switch_callback = None
        self._rotate_callback = None

    def setup(self):
        if self._is_setup:
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup([self._switch], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            self._switch,
            GPIO.RISING,
            callback=self._on_switch,
            bouncetime=200,
        )
        GPIO.setup([self._a, self._b], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._a, GPIO.BOTH, callback=self._on_rotate, bouncetime=50)
        GPIO.add_event_detect(self._b, GPIO.BOTH, callback=self._on_rotate, bouncetime=50)

        self._is_setup = True

    def shutdown(self):
        if not self._is_setup:
            return

        GPIO.remove_event_detect(self._switch)
        GPIO.remove_event_detect(self._a)
        GPIO.remove_event_detect(self._b)

    def on_switch(self, callback):
        """
        Set a callback for when the rotary encoder's switch is pressed.

        :param callback: A callback function without arguments.
        """
        self._switch_callback = callback

    def off_switch(self):
        """
        Remove the used switch callback.
        """
        self._switch_callback = None

    def on_rotate(self, callback):
        """
        Set a callback for when the rotary encoder's knob is turned.

        :param callback: A callback function expecting a direction argument,
            which will either be CLOCKWISE or COUNTERCLOCKWISE.
        """
        self._rotate_callback = callback

    def off_rotate(self):
        """
        Remove the used rotation callback.
        """
        self._rotate_callback = None

    def _on_switch(self, pin):
        if self._switch_callback:
            self._switch_callback()

    def _on_rotate(self, pin):
        step = (GPIO.input(self._a), GPIO.input(self._b))
        if step == self._step:
            return

        direction = self._get_direction(step)
        self._moved += direction
        self._step = step

        # back to first step?
        if step == self.STEPS[0]:
            # full run in one direction completed?
            if abs(self._moved) == len(self.STEPS) and self._rotate_callback:
                self._rotate_callback(direction)

            self._moved = 0

    def _get_direction(self, step):
        num_steps = len(self.STEPS)
        step_idx = self.STEPS.index(step)
        start_idx = self.STEPS.index(self._step)
        next_idx = (start_idx + 1) % num_steps
        if step_idx == next_idx:
            return self.CLOCKWISE

        prev_idx = (start_idx - 1 + num_steps) % num_steps
        if step_idx == prev_idx:
            return self.COUNTERCLOCKWISE

        return self.UNDECIDED
