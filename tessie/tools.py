""" Various tools for running tests """

import re
import socket
import subprocess

from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Union,
)

import internal


def exec_command(
        command: str,
        background: bool = False,
        output: Union[int, str] = subprocess.PIPE,
        shell: bool = False
) -> Union[subprocess.Popen, Tuple[str, str]]:
    """ Execute a command

    Returns with a tuple of stdout and stderr or with a handle to process
    if it is run in the background

    :output:    a filepath given as string or e.g. `subprocess.PIPE` (default value)
    """

    if command in ["", None]:
        raise RuntimeError("Command cannot be empty or `None`")

    if isinstance(output, str):
        if not background:
            raise RuntimeError("Cannot write output to file unless the process runs in background")

    try:
        process = internal.exec_command(command, output, shell)

        if not background:
            return process.communicate()
    except KeyboardInterrupt:
        process.terminate()

    return process


def send_tcp(address: str, data: Union[bytes, str], expect_answer: bool = True) -> Optional[bytes]:
    """ Send data to an address via TCP

    :address:   must be given in a format like 'localhost:8000'
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = address.split(":")
    server_address = (host, int(port))

    try:
        client_socket.connect(server_address)
        client_socket.sendall(data.encode() if isinstance(data, str) else data)
        if not expect_answer:
            return None
        return client_socket.recv(1024)
    finally:
        client_socket.close()


def expect_eq(lhs: Any, rhs: Any) -> bool:
    """ Expect equality between `lhs` and `rhs` """
    return internal.test_expectation(lhs == rhs, message = f"{lhs} == {rhs}")


def expect_gt(lhs: Any, rhs: Any) -> bool:
    """ Expect `lhs` to be greater than `rhs` """
    return internal.test_expectation(lhs > rhs, message = f"{lhs} > {rhs}")


# TODO(feat): implement the rest of the combination of `expect_` functions


def check_file(path: str, func: Callable[[List[str]], bool]) -> Tuple[bool, str]:
    """ Checks the content of a file according to `func`

    `func` receives the lines stripped of leading and trailing whitespace of
    the file as a list
    """

    try:
        with open(path, "r", encoding="utf-8") as inf:
            lines = inf.readlines()
            success = func(list(map(lambda x: x.strip(), lines)))
            return (success, "".join(lines))
    except FileNotFoundError as ex:
        internal.log_failure(str(ex), "Exception")
        return (False, "")


def file_contains_pattern(path: str, pattern: str, verbose: bool = False) -> bool:
    """ Checks whether the file contains a `pattern` given by regex """
    # TODO(feat): decouple from file, it should work with simple strings
    log_args = {
        "message": pattern,
        "matcher": "File line pattern",
        "additional_message": path
    }

    success, content = check_file(
        path,
        lambda lines: any(map(lambda line: re.match(pattern, line) is not None, lines))
    )

    return internal.test_file_exceptation(success, content, verbose, **log_args)


def file_contains_line(path: str, pattern: str, verbose: bool = False) -> bool:
    """ Checks whether the file contains a given line """
    # TODO(feat): decouple from file, it should work with simple strings
    log_args = {
        "message": pattern,
        "matcher": "File exact line",
        "additional_message": path
    }

    success, content = check_file(
        path,
        lambda lines: any(map(lambda line: pattern == line, lines))
    )

    return internal.test_file_exceptation(success, content, verbose, **log_args)
