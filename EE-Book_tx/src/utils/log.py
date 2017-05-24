#!/usr/bin/env python
# This file is Python 2 compliant.

u"""
steal from you-get, TODO: LICENSE
"""

import os
import sys

IS_ANSI_TERMINAL = os.getenv('TERM') in (
    'eterm-color',
    'linux',
    'screen',
    'vt100',
    'xterm',
)

# ANSI escape code
# See <http://en.wikipedia.org/wiki/ANSI_escape_code>
RESET = 0
BOLD = 1
UNDERLINE = 4
NEGATIVE = 7
NO_BOLD = 21
NO_UNDERLINE = 24
POSITIVE = 27
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
LIGHT_GRAY = 37
DEFAULT = 39
BLACK_BACKGROUND = 40
RED_BACKGROUND = 41
GREEN_BACKGROUND = 42
YELLOW_BACKGROUND = 43
BLUE_BACKGROUND = 44
MAGENTA_BACKGROUND = 45
CYAN_BACKGROUND = 46
LIGHT_GRAY_BACKGROUND = 47
DEFAULT_BACKGROUND = 49
DARK_GRAY = 90                  # xterm
LIGHT_RED = 91                  # xterm
LIGHT_GREEN = 92                # xterm
LIGHT_YELLOW = 93               # xterm
LIGHT_BLUE = 94                 # xterm
LIGHT_MAGENTA = 95              # xterm
LIGHT_CYAN = 96                 # xterm
WHITE = 97                      # xterm
DARK_GRAY_BACKGROUND = 100      # xterm
LIGHT_RED_BACKGROUND = 101      # xterm
LIGHT_GREEN_BACKGROUND = 102    # xterm
LIGHT_YELLOW_BACKGROUND = 103   # xterm
LIGHT_BLUE_BACKGROUND = 104     # xterm
LIGHT_MAGENTA_BACKGROUND = 105  # xterm
LIGHT_CYAN_BACKGROUND = 106     # xterm
WHITE_BACKGROUND = 107          # xterm


def sprint(text, *colors):
    u"""
    Format text with color or other effects into ANSI escaped string.
    :param text:
    :param colors:
    :return:
    """
    return "\33[{}m{content}\33[{}m".format(";".join([str(color) for color in colors]), RESET, content=text) \
        if IS_ANSI_TERMINAL and colors else text


def println(text, *colors):
    u"""
    Print text to standard output.
    :param text:
    :param colors:
    :return:
    """
    sys.stdout.write(sprint(text, *colors) + "\n")


def print_err(text, *colors):
    u"""
    Print text to standard error.
    :param text:
    :param colors:
    :return:
    """
    sys.stderr.write(sprint(text, *colors) + "\n")


def print_log(text, *colors):
    u"""
    Print a log message to standard error.
    :param text:
    :param colors:
    :return:
    """
    sys.stderr.write(sprint("{}".format(text), *colors) + "\n")


def info_log(message):
    u"""
    Print a normal log message.
    :param message:
    :return:
    """
    print_log(message)


def debug_log(message):
    u"""
    Print a debug log message.
    :param message:
    :return:
    """
    print_log(message, BLUE)


def warning_log(message):
    u"""
    Print a warning log message.
    :param message:
    :return:
    """
    print_log(message, YELLOW)


def error_log(message, exit_code=None):
    u"""
    Print an error log message.
    :param message:
    :param exit_code:
    :return:
    """
    print_log(message, YELLOW, BOLD)
    if exit_code is not None:
        exit(exit_code)


def wtf_log(message, exit_code=1):
    u"""
    What a Terrible Failure!
    :param message:
    :param exit_code:
    :return:
    """
    print_log(message, RED, BOLD)
    if exit_code is not None:
        exit(exit_code)
