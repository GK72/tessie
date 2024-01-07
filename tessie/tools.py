""" Various tools for running tests """

import re
import socket
import subprocess

from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

import docker

import internal


def docker_client() -> docker.DockerClient:
    """ Convenience function to get Docker client """
    return docker.from_env()


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


def start_container(
        image: str,
        ports: Optional[Dict[str, int]] = None
) -> docker.models.containers.Container:
    """ Wrapper around `docker.containers.run(...)`

    :ports:  map ports to host ports
             container port must be given in `port/protocol` format, i.e. "8080/tcp"
    """
    return docker_client().containers.run(image, auto_remove=True, detach=True, ports=ports)


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


def match(
    pattern: str,
    content: str,
    verbose: bool = False,
    matcher: str = "String matcher",
    **kwargs: Any
) -> bool:
    """ Check for match on any line in a given content """
    return internal.test_expectation(
        internal.check_str(content, lambda line: re.match(pattern, line) is not None),
        content=content,
        message=pattern,
        verbose=verbose,
        matcher=matcher,
        **kwargs
    )


def contains_line(
    what: str,
    content: Union[str, bytes],
    verbose: bool = False,
    matcher: str = "String contains line",
    **kwargs: Any
) -> bool:
    """ Check for exact line in a given content """
    return internal.test_expectation(
        internal.check_str(content, lambda line: what == line),
        content=content,
        message=what,
        verbose=verbose,
        matcher=matcher,
        **kwargs
    )


def file_match(pattern: str, path: str, verbose: bool = False) -> bool:
    """ Check for match on any line in a given file """
    return match(
        pattern,
        internal.readfile(path),
        verbose,
        additional_message=path,
        matcher="File line matcher"
    )


def file_contains_line(pattern: str, path: str, verbose: bool = False) -> bool:
    """ Check for exact line in a given file """
    return contains_line(
        pattern,
        internal.readfile(path),
        verbose,
        additional_message=path,
        matcher="File contains line"
    )
