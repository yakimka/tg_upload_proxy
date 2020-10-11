from argparse import ArgumentTypeError
from unittest.mock import Mock

import pytest

from tg_upload_proxy.utils import argparse
from tg_upload_proxy.utils.argparse import validate, positive_int, clear_environ


@pytest.mark.parametrize('value,expected', [
    (123, 123),
    ('345', 345),
    (5.5, 5),
    (-1, -1),
    ('-100', -100),
    ('0', 0),
])
class TestValidate():
    def test_cast_to_int(self, value, expected):
        validator = validate(int, lambda x: True)

        assert expected == validator(value)

    def test_fail_constrait(self, value, expected):
        validator = validate(int, lambda x: False)

        with pytest.raises(ArgumentTypeError):
            validator(value)


@pytest.mark.parametrize('value,expected', [
    (123, 123),
    ('345', 345),
    (5.5, 5),
])
def test_positive_int_with_positive_values(value, expected):
    assert expected == positive_int(value)


@pytest.mark.parametrize('value,expected', [
    (-1, -1),
    ('-100', -100),
    ('0', 0),
])
def test_positive_int_with_not_positive_values(value, expected):
    with pytest.raises(ArgumentTypeError):
        positive_int(value)


def test_clear_environ(monkeypatch):
    mos = Mock()
    monkeypatch.setattr(argparse, 'os', mos)
    mos.environ = {
        1: '1',
        2: '2',
        3: '3'
    }

    clear_environ(lambda x: x != 2)

    assert {2: '2'} == mos.environ
