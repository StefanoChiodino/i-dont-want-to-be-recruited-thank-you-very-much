import os
from typing import List
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pytest

import main


class TestArgParser:
    def test_parsing_add(self) -> None:
        args = main._parse_args("add domain.com".split(" "))
        assert args

    def test_parsing_remove(self) -> None:
        args = main._parse_args("remove domain.com".split(" "))
        assert args

    def test_parsing_export(self) -> None:
        args = main._parse_args("export".split(" "))
        assert args


class TestAdd:
    @mock.patch("builtins.open")
    @pytest.mark.parametrize("domains", [
        ["domain.com"],
        ["email.domain.com"],
        ["domain.com", "email.domain.com"],
    ])
    def test_add_succesfully(self, open_mock: MagicMock, domains: str):
        for domain in domains:
            main.add(domain)
        assert open_mock.return_value.__enter__.return_value.writelines.call_count == len(domains)

    @mock.patch("builtins.open")
    @pytest.mark.parametrize("start,domain_to_remove,end", [
        (["email.domain.com"], "email.domain.com", []),
        (["domain.com"], "domain.com", []),
        (["domain.com", "email.domain.com"], "email.domain.com", ["domain.com"]),
    ])
    def test_remove_succesfully(self, open_mock: MagicMock, start: List[str], domain_to_remove: str, end: List[str]):
        open_mock.return_value.__enter__.return_value.readlines.return_value = start
        main.remove(domain_to_remove)
        assert open_mock.return_value.__enter__.return_value.writelines.call_args_list[0][0][0] == end

    @mock.patch("builtins.open")
    def test_remove_not_existing_throws(self, open_mock: MagicMock):
        open_mock.return_value.__enter__.return_value.readlines.return_value = ["domain.com"]
        with pytest.raises(ValueError):
            main.remove("email.domain.com")
