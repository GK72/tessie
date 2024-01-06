from enum import Enum


class AnsiColors(Enum):
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


def colorize(color: str, message: str):
    """ Colorize a message and set the color back to default """
    return f"{color}{message}{AnsiColors.DEFAULT.value}"


def log_success(message: str, matcher: str = "", additional_message: str = ""):
    print(
           "{}".format(colorize(AnsiColors.GREEN.value, "[  OK  ]"))
        + " {}".format(colorize(AnsiColors.PURPLE.value, matcher))
        + " {}".format(colorize(AnsiColors.WHITE.value, message))
        + "   {}".format(colorize(AnsiColors.DARK_GREY.value, additional_message))
    )


def log_failure(message: str, matcher: str = "", additional_message: str = ""):
    print(
           "{}".format(colorize(AnsiColors.RED.value, "[FAILED]"))
        + " {}".format(colorize(AnsiColors.PURPLE.value, matcher))
        + " {}".format(colorize(AnsiColors.WHITE.value, message))
        + "   {}".format(colorize(AnsiColors.DARK_GREY.value, additional_message))
    )


def test_expectation(success: bool, **kwargs) -> bool:
    """ Wrapping automatic logging

    :kwargs:    must match with parameters of the log functions
    """

    if success:
        log_success(**kwargs)
    else:
        log_failure(**kwargs)
    return success


def test_file_exceptation(success: bool, content: str, verbose=False, **kwargs) -> bool:
    """ Wrapping automatic logging for file matchers

    In case of failure, the content of the file is also logged

    :kwargs:    must match with parameters of the log functions
    """

    if verbose and not success:
        kwargs["additional_message"] += "\n{}".format("".join(content))
    return test_expectation(success, **kwargs)
