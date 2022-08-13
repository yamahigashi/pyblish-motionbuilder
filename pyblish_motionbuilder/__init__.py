from .version import *  # type: ignore  # noqa:F401,F403

from .lib import (
    show,
    setup,
    teardown,
    register_plugins,
    register_host,
    add_to_filemenu,
    dock,

    # Utility functions
    maintained_selection
)


def is_setup():
    from . import lib
    return lib._has_been_setup  # type: ignore


__all__ = [
    "show",
    "setup",
    "teardown",
    "register_plugins",
    "register_host",
    "add_to_filemenu",
    "dock",

    "maintained_selection",
    # "maintained_time",
]
