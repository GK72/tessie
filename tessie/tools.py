""" Various tools for running tests """

import shlex
import subprocess

from typing import Any
from typing import Union
from typing import Tuple

def exec_command(command: str, background: bool = False, shell: bool = False) \
        -> Union[subprocess.Popen, Tuple[str, str]]:
    """ Execute a command

    Returns with a tuple of stdout and stderr or with a handle to process
    if it is run in the background
    """

    if command in ["", None]:
        raise RuntimeError("Command cannot be empty or `None`")

    try:
        process = subprocess.Popen(                                                                 # pylint: disable=R1732,C0301 # caller should close the process in case of running it in background
            shlex.split(command),
            text=True,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if not background:
            return process.communicate()
    except KeyboardInterrupt:
        process.terminate()

    return process


def check(lhs: Any, rhs: Any) -> bool:
    """ Check for equality, log whether it is successful """

    if lhs == rhs:
        print(f"OK: {lhs} == {rhs}")        # TODO: logging, no raw printing
        return True

    print(f"FAIL: {lhs} == {rhs}")          # TODO: logging, no raw printing
    return False
