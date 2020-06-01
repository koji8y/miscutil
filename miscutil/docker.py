"""Utilities for docker."""
from typing import List
from typing import Optional

from time import sleep

from miscutil import conj
from miscutil.subprocess import CommandResult
from miscutil import disj
from miscutil import ijoin
from miscutil.subprocess import run_command


class DockerCompose:
    """docker-compose invoker."""
    def __init__(self, on_directory: Optional[str] = None):
        self.on_directory = on_directory

    def run_command(
            self,
            *args: str,
            print_progress: bool = False) -> CommandResult:
        """invoke docker-compose."""
        if print_progress:
            print('dcs{}'.format(args))
        return run_command(
            list(ijoin('docker-compose', *args)),
            cwd=self.on_directory)

    @staticmethod
    def _running_normally(
            result: CommandResult,
            mandatory_words: List[str]) -> bool:
        """check if docker container is running normally."""
        return disj(lambda line: conj(lambda word: word in line,
                                      mandatory_words),
                    result.stdout.split('\n'))

    def up_in_background(  # pylint: disable=too-many-arguments
            self,
            cmd_args: List[str],
            mandatory_words: List[str],
            max_count: int = 10,
            check_interval_in_sec: float = 0.25,
            print_progress: bool = False) -> CommandResult:
        """Boot up service."""
        # Check if the docker container is already running.
        result = self.run_command(*cmd_args)
        if self._running_normally(result, mandatory_words):
            return result

        result = self.run_command('up', '-d', print_progress=print_progress)
        if not result.normal_end:
            return result
        result = self.run_command(*cmd_args)
        timeout = max_count
        while timeout > 0 and not self._running_normally(result,
                                                         mandatory_words):
            if print_progress:
                print('waiting container is ready ({}/{})...'.format(
                    1 + max_count - timeout, max_count))
            sleep(check_interval_in_sec)
            timeout -= 1
            result = self.run_command(*cmd_args)
        if timeout <= 0:
            result.normal_end = False
        if print_progress:
            print('{}'.format(result))
        return result

    def down(self, print_progress: bool = False) -> CommandResult:
        """Shut down service."""
        return self.run_command('down', print_progress=print_progress)
