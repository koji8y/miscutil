"""Utility library for json and yaml with intermediate expression."""
from typing import Any
from typing import Dict
from typing import Collection, List
from typing import Optional
from typing import Tuple

from collections.abc import Mapping as ABCMapping  # type: ignore
from enum import Enum
import json
from unittest import TestCase
import yaml

from miscutil import none_or

KEY_NAME_FOR_TYPE = " type"


def json_obj2yaml_str(in_json_obj: Any, sort_keys: bool = True) -> str:
    """convert JSON object to YAML string."""
    return yaml.dump(JSONEncoder(show_type=False).to_json(in_json_obj),
                     sort_keys=sort_keys)


def json2yaml(in_json: str, sort_keys: bool = True) -> str:
    """convert string in JSON to string in YAML."""
    return yaml.dump(json.loads(in_json), sort_keys=sort_keys)


def json2yaml_lines(in_json: str, sort_keys: bool = True) -> List[str]:
    """convert string in JSON to string in YAML."""
    return json2yaml(in_json=in_json, sort_keys=sort_keys).split("\n")


def to_json_using_slot(
        self,
        attr_names: List[str] = None,
        using_to_json: Collection[str] = None,
        with_key_name: bool = True) -> Dict[str, Any]:
    """convert object having to_json method to JSON."""
    obj: Dict[str, Any] = ({KEY_NAME_FOR_TYPE: self.__class__.__name__}
                           if with_key_name else
                           {})
    if attr_names is None:
        attr_names = self.__slot__
    for attr_name in attr_names:
        val = getattr(self, attr_name)
        if val is not None and (using_to_json is not None and
                                attr_name in using_to_json):
            obj.update({attr_name: val.to_json()})
        else:
            obj.update({attr_name: val})
    return obj


class JSONEncoder(json.JSONEncoder):
    """JSON encoder for classes that have method 'to_json'."""
    def __init__(self, *,
                 skipkeys=False, ensure_ascii=True, check_circular=True,
                 allow_nan=True, sort_keys=False, indent=None,
                 separators=None, default=None,
                 other_encoder=None,
                 show_type: bool = True,
                 show_zero_value: bool = False):
        super().__init__(
            skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan,
            sort_keys=sort_keys, indent=indent,
            separators=separators, default=default)
        self.other_encoder = other_encoder
        self.show_type = show_type
        self.show_zero_value = show_zero_value

    # pylint: disable=method-hidden, arguments-differ
    def default(self, target: Any) -> Any:
        to_json = None
        if hasattr(target, "to_json"):
            to_json = getattr(target, "to_json")
        elif hasattr(target, "to_dict"):
            to_json = getattr(target, "to_dict")
        if to_json is not None:
            obj = to_json()
            if not self.show_type and KEY_NAME_FOR_TYPE in obj:
                obj.pop(KEY_NAME_FOR_TYPE)
            if not self.show_zero_value and hasattr(obj, "items"):
                return {key: value for key, value in obj.items() if value}
            return obj
        treated, obj = self.treat_primitive(target)
        if treated:
            return obj
        try:
            if self.other_encoder is not None:
                return self.other_encoder.default(target)
            return super().default(target)
        except TypeError as ex:
            return "{} for {} - {}: {}".format(
                type(ex), type(target), ex, target)

    @staticmethod
    def treat_primitive(obj: Any) -> Tuple[bool, Any]:
        """convert some type of primitive instance to json."""
        if isinstance(obj, Enum):
            return True, obj.name
        if isinstance(obj, ABCMapping):
            # return (True, {key: value for key, value in obj.items()})
            return (True, dict(obj))
        if isinstance(obj, set):
            return (True, list(obj))
        return False, None

    def to_json(self, obj: Any) -> Dict[str, Any]:
        """convert an object to json"""
        return json.loads(json.dumps(
            obj, ensure_ascii=False, default=self.default, sort_keys=True))

    def to_yaml_str(self, obj: Any) -> str:
        """convert an object to yaml string"""
        return json_obj2yaml_str(self.to_json(obj))

    def to_yaml_lines(self, obj: Any) -> List[str]:
        """convert an object to yaml lines"""
        return self.to_yaml_str(obj).split("\n")

    def assertJsonEqualAsYaml(  # pylint: disable=invalid-name
            self,
            testCase: TestCase,
            practical: Any,
            expected: Any,
            memo: Optional[str] = None) -> None:
        """assert equality of objects in JSON format."""
        return testCase.assertSequenceEqual(
            self.to_yaml_lines(practical), self.to_yaml_lines(expected),
            # msg=none_or(memo, lambda msg: '\n{}'.format(msg)))
            msg=none_or(memo, '\n{}'.format))


def to_yaml_str(obj: Any,
                show_type: bool = False,
                show_zero_value: bool = False) -> str:
    """convert an object to yaml string"""
    return JSONEncoder(show_type=show_type,
                       show_zero_value=show_zero_value).to_yaml_str(obj)


def print_as_yaml_str(obj: Any,
                      show_type: bool = False,
                      show_zero_value: bool = False) -> None:
    """print an object in yaml format."""
    print(to_yaml_str(
        obj, show_type=show_type, show_zero_value=show_zero_value))


def obj_to_json(obj: Any,
                show_type: bool = False,
                show_zero_value: bool = False) -> Any:
    """convert an object to json object"""
    return JSONEncoder(show_type=show_type,
                       show_zero_value=show_zero_value).to_json(obj)
