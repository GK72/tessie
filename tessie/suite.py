""" Tessie Test Suite """

from typing import (
    Callable,
    Dict
)

import internal
from internal import AnsiColors


class Suite:
    """ Test suite holding the test cases """

    def __init__(self, name: str) -> None:
        """ Create a suite with a name """
        self._suite_name = name
        self._test_cases: Dict[str, Callable[[], bool]] = {}
        self._is_all_success = True

    def test_case(self, name: str, func: Callable[[], bool]) -> None:
        """ Add a named test case """
        self._test_cases[name] = func

    def run(self) -> bool:
        """ Run all test cases with measuring the time the test cases take """
        for test_name, test_case in self._test_cases.items():
            success = self._timed_run(test_name, test_case)
            if not success:
                self._is_all_success = False

        return self._is_all_success

    def _timed_run(self, name: str, func: Callable[[], bool]) -> bool:
        print(internal.colorize(AnsiColors.BOLD_BLUE.value, f"TEST CASE: {name}"))

        # TODO(refact): decorate with stopwatch
        stopwatch = internal.StopWatch()
        stopwatch.start()
        success = func()
        elapsed = stopwatch.stop()

        self._log_result(name, elapsed, success)
        return success

    def _log_result(self, name: str, elapsed: float, success: bool) -> None:
        if success:
            self._log_success(name, elapsed)
        else:
            self._log_failure(name, elapsed)

    def _log_success(self, name: str, elapsed: float) -> None:
        self._log_impl(True, name, elapsed)

    def _log_failure(self, name: str, elapsed: float) -> None:
        self._log_impl(False, name, elapsed)

    def _log_impl(self, success: bool, name: str, elapsed: float) -> None:
        if success:
            color = AnsiColors.BOLD_GREEN.value
            tag = "OK"
        else:
            color = AnsiColors.BOLD_RED.value
            tag = "FAILED"

        print(
            internal.colorize(color, f"TEST CASE {tag}: {name}"),
            internal.colorize(AnsiColors.DARK_GREY.value, f"(elapsed: {elapsed:.3}s)")
        )
