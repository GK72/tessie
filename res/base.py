import argparse
import subprocess
import time

from typing import Tuple

import tools


def start_server(port: int) -> subprocess.Popen:
    """ Start a server on the given port responding with the
    conent given in a file """

    return tools.exec_command(f"res/run_server.sh {port}", background=True, shell=False)

    # FIXME: Running commands with shell set to True
    #  return tools.exec_command(f"nc -l -p {port} -c localhost <<< {response}", background=True, shell=True)


def send_request(port: int) -> Tuple[str, str]:
    """ Returns stdout and stderr of curl """
    return tools.exec_command(f"curl --silent localhost:{port}")


def run_test(test_args: dict):
    parser = argparse.ArgumentParser()
    parser.add_argument("--port")
    args = parser.parse_args(test_args)

    server = start_server(args.port)
    time.sleep(0.5)

    result = send_request(args.port)
    server.terminate()

    if not tools.check(result[0].strip(), "Hello, Tessie!"):
        print(result[1])
