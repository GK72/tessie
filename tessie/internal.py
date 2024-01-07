""" Tessie implementation details """

import shlex
import subprocess

from enum import Enum

from typing import (
    Any,
    Union
)


class AnsiColors(Enum):
    """ ANSI escape codes for colors """
    DARK_GREY = "\x1b[30;1m"
    RED       = "\x1b[31;20m"
    BOLD_RED  = "\x1b[31;1m"
    GREEN     = "\x1b[32;20m"
    YELLOW    = "\x1b[33;20m"
    BLUE      = "\x1b[34;20m"
    PURPLE    = "\x1b[35;20m"
    CYAN      = "\x1b[36;20m"
    WHITE     = "\x1b[37;1m"
    GREY      = "\x1b[38;20m"
    DEFAULT   = "\x1b[0m"


def colorize(color: str, message: str) -> str:
    """ Colorize a message and set the color back to default """
    return f"{color}{message}{AnsiColors.DEFAULT.value}"


def log_success(message: str, matcher: str = "", additional_message: str = "") -> None:
    """ Log a successful check with green OK tag """
    # pragma pylint: disable=C0209
    print(
           "{}".format(colorize(AnsiColors.GREEN.value, "[  OK  ]"))
        + " {}".format(colorize(AnsiColors.PURPLE.value, matcher))
        + " {}".format(colorize(AnsiColors.WHITE.value, message))
        + "   {}".format(colorize(AnsiColors.DARK_GREY.value, additional_message))
    )
    # pragma pylint: enable=C0209


def log_failure(message: str, matcher: str = "", additional_message: str = "") -> None:
    """ Log a failure with red FAILED tag """
    # pragma pylint: disable=C0209
    print(
           "{}".format(colorize(AnsiColors.RED.value, "[FAILED]"))
        + " {}".format(colorize(AnsiColors.PURPLE.value, matcher))
        + " {}".format(colorize(AnsiColors.WHITE.value, message))
        + "   {}".format(colorize(AnsiColors.DARK_GREY.value, additional_message))
    )
    # pragma pylint: enable=C0209


def test_expectation(success: bool, **kwargs: Any) -> bool:
    """ Wrapping automatic logging

    :kwargs:    must match with parameters of the log functions
    """

    if success:
        log_success(**kwargs)
    else:
        log_failure(**kwargs)
    return success


def test_file_exceptation(
        success: bool,
        content: str,
        verbose: bool = False,
        **kwargs: Any
) -> bool:
    """ Wrapping automatic logging for file matchers

    In case of failure, the content of the file is also logged

    :kwargs:    must match with parameters of the log functions
    """

    if verbose and not success:
        kwargs["additional_message"] += content
    return test_expectation(success, **kwargs)


def exec_command(
        command: str,
        output: Union[int, str] = subprocess.PIPE,
        shell: bool = False
) -> subprocess.Popen:
    """ Internal helper function to handle redirection of stdout and stderr to file """

    if isinstance(output, str):
        with open(output, "w", encoding="utf-8") as outf:
            return subprocess.Popen(
                shlex.split(command),
                text=True,
                shell=shell,
                stdout=outf,
                stderr=outf
            )

    return subprocess.Popen(
        shlex.split(command),
        text=True,
        shell=shell,
        stdout=output,
        stderr=output
    )