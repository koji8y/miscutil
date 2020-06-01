"""Utility library for test."""
from typing import Any
from pathlib import Path
import unittest
import yaml

from miscutil import yamljson


class TCWithGoldenFile(unittest.TestCase):
    """"Abstract test case using golden files."""
    def __init__(self,
                 *,
                 top_dir: str,
                 suffix_of_golden: str,
                 out_extension: str = 'yaml',
                 method_name: str = 'runTest'):
        super().__init__(method_name)
        self.maxDiff = None  # pylint: disable=invalid-name
        self.top_dir = top_dir
        self.suffix_of_golden = suffix_of_golden
        self.out_extension = out_extension

    def _full_path(self, rel_path: str, *args, **kwargs) -> str:
        return str(Path(self.top_dir, rel_path.format(*args, **kwargs)))

    def _input_yaml_path(self, core: str) -> str:
        return self._full_path('input/{}.yaml', core)

    def _golden_yaml_path(self, core: str) -> str:
        return self._full_path(
            'golden/{brace}.{suffix_of_golden}.{extension}'.format(
                brace='{}',
                suffix_of_golden=self.suffix_of_golden,
                extension=self.out_extension),
            core)

    def _memo_on_golden_file_path(self,
                                  core_of_input: str,
                                  core_of_golden: str) -> str:
        return 'input_path={}\ngolden_path={}'.format(
            self._input_yaml_path(core_of_input),
            self._golden_yaml_path(core_of_golden))

    def _put_asis_n_get_expected(
            self,
            asis_obj: Any,
            core_of_golden: str,
            convert_from_to_yaml: bool = True) -> Any:
        with open(self._golden_yaml_path(core_of_golden)) as yfile:
            if convert_from_to_yaml:
                expected_obj = yaml.load(yfile, Loader=yaml.FullLoader)
            else:
                expected_obj = yfile.read()
        with open(
                self._golden_yaml_path('{}.asis'.format(core_of_golden)),
                'w') as yfile:
            if convert_from_to_yaml:
                print(yamljson.json_obj2yaml_str(asis_obj), file=yfile)
            else:
                print(asis_obj, file=yfile)
        return expected_obj
