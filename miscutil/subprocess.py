"""Utilities for subprocess"""
from typing import Any, Dict, List, Optional

from datetime import datetime
from enum import Enum
import subprocess

from miscutil.yamljson import to_yaml_str


class Duration:
    """Execution duration manager."""
    class _Status(Enum):
        """Sort of execution status."""
        NotStarted = "NotStarted"
        Started = "Started"
        Finished = "Finished"

    def __init__(self):
        self.status = self._Status.NotStarted
        self.time_start = datetime.min
        self.time_end = datetime.min

    def __enter__(self) -> "Duration":
        self.status = self._Status.Started
        self.time_start = datetime.now()
        return self

    def __exit__(self, status, ex_str, traceback_info) -> None:
        self.time_end = datetime.now()
        self.status = self._Status.Finished

    @property
    def in_seconds(self) -> float:
        """get consumed time in seconds."""
        if self.status != self._Status.Finished:
            return 0.0
        return (self.time_end - self.time_start).total_seconds()


class CommandResult:
    """Summarized command execution result."""
    __slot__ = [
        'normal_end',
        'returncode',
        'stdout',
        'stderr']

    def __init__(self, result: subprocess.CompletedProcess):
        self.normal_end = result.returncode == 0
        self.returncode = result.returncode
        self.stdout = '' if result.stdout is None else result.stdout.decode(
            'utf8')
        self.stderr = '' if result.stderr is None else result.stderr.decode(
            'utf8')

    def to_dict(self) -> Dict[str, Any]:
        """get dict type version of this object."""
        return {name: getattr(self, name) for name in self.__slot__}

    def __repr__(self) -> str:
        return to_yaml_str(self.to_dict())


def run_command(
        cmd_args: List[str],
        show_process: bool = False,
        cwd: Optional[str] = None) -> CommandResult:
    """invoke command.
    Note you make sure return code is zero by yourself.
    """
    if show_process:
        print(' '.join(cmd_args))
    # pylint: disable=subprocess-run-check
    completed_process = subprocess.run(
        list(cmd_args),
        # capture_output=True,  # This is valid only after 3.7.
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        # text=True,  # This is valid only after 3.7.
        cwd=cwd)
    return CommandResult(completed_process)
