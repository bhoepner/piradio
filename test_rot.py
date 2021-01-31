#!/usr/bin/env python3

from time import sleep
from RPi import GPIO

PIN_A = 22
PIN_B = 27
DELAY = 0.001
STEPS_PER_CLICK = 4


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([PIN_A, PIN_B], GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_pins():
    return GPIO.input(PIN_A), GPIO.input(PIN_B)


def sign(num):
    return -1 if num < 0 else 1


def update(prev_a, prev_b, prev_delta):
    """
     prev_a | prev_b | a | b | delta
    --------+--------+---+---+-------
          0 |      0 | 1 | 0 |    +1
          0 |      1 | 0 | 0 |    +1
          1 |      0 | 1 | 1 |    +1
          1 |      1 | 0 | 1 |    +1     prev_a == b and prev_b != a
          0 |      0 | 0 | 1 |    -1
          0 |      1 | 1 | 1 |    -1
          1 |      0 | 0 | 0 |    -1
          1 |      1 | 1 | 0 |    -1     prev_a != b and prev_b == a
          0 |      0 | 0 | 0 |     0
          0 |      1 | 0 | 1 |     0
          1 |      0 | 1 | 0 |     0
          1 |      1 | 1 | 1 |     0     prev_a == a and prev_b == b
          0 |      0 | 1 | 1 |   +-2
          0 |      1 | 1 | 0 |   +-2
          1 |      0 | 0 | 1 |   +-2
          1 |      1 | 0 | 0 |   +-2     prev_a != a and prev_b != b
    """
    a, b = read_pins()
    delta = 0

    if prev_a == b and prev_b != a:
        delta = 1
    elif prev_a != b and prev_b == a:
        delta = -1
    elif prev_a != a and prev_b != b:
        # keep previous direction when two steps are done
        delta = 2 * sign(prev_delta)

    return a, b, delta


def loop():
    a, b = read_pins()
    delta = 0
    clicks = 0

    while True:
        a, b, delta = update(a, b, delta)
        if delta != 0 and a == 0 and b == 0:
            clicks = sign(delta)

        if clicks != 0:
            print('rotation:', clicks)
            clicks = 0

        sleep(DELAY)


def main():
    setup()
    loop()


if __name__ == '__main__':
    main()
