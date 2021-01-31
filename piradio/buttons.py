"""
This is just a wrapper module for `phatbeat` button handling.

Sadly `phatbeat` misses the functionality to _remove_ button handlers, which
the project requires. This is what the functions `off` and `off_hold` are for.
"""
import phatbeat

BTN_MENU = phatbeat.BTN_PLAYPAUSE
BTN_NEXT = phatbeat.BTN_FASTFWD
BTN_PREV = phatbeat.BTN_REWIND
BTN_VOLUP = phatbeat.BTN_VOLUP
BTN_VOLDN = phatbeat.BTN_VOLDN
BTN_POWER = phatbeat.BTN_ONOFF

BTN_ALL = [BTN_MENU, BTN_NEXT, BTN_PREV, BTN_VOLUP, BTN_VOLDN, BTN_POWER]

on = phatbeat.on
on_hold = phatbeat.hold


def off(buttons):
    """
    Remove all button "on" handlers for the given list of buttons.
    """
    phatbeat.setup()
    for button in _to_iter(buttons):
        phatbeat._button_handlers.pop(button, None)
        phatbeat._button_repeat.pop(button, None)


def off_hold(buttons):
    """
    Remove all button "on_hold" handlers for the given list of buttons.
    """
    phatbeat.setup()
    for button in _to_iter(buttons):
        phatbeat._button_hold_handlers.pop(button, None)
        phatbeat._button_hold_repeat.pop(button, None)
        phatbeat._button_hold_time.pop(button, None)


def _to_iter(buttons):
    try:
        return iter(buttons)
    except TypeError:
        return iter([buttons])
