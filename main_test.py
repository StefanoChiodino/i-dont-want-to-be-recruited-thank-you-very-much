import os
from datetime import datetime, date
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

    @mock.patch("builtins.open")
    def test_export(self, open_mock: MagicMock):
        open_mock.return_value.__enter__.return_value.readlines.return_value = ["domain.com", "email.domain.com"]
        open_mock.return_value.__enter__.return_value.read.return_value = """
        <?xml version='1.0' encoding='UTF-8'?>
        <feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
            <title>{{ title }}</title>
            <id>{{ id }}</id>
            <updated>{{ updated }}</updated>
            {% if author %}
            <author>
                <name>{{ author.name }}</name>
                <email>{{ author.email }}</email>
            </author>
            {% endif %}
            {% for entry in entries %}
            <entry>
                <category term='filter'></category>
                <title>{{ entry.title }}</title>
                <id>{{ entry.id }}</id>
                <updated>{{ entry.updated }}</updated>
                <content></content>
                <apps:property name='from' value='{{ entry.from }}'/>
                <apps:property name='label' value='Recruitment'/>
                <apps:property name='sizeOperator' value='s_sl'/>
                <apps:property name='sizeUnit' value='s_smb'/>
            </entry>
            {% endfor %}
        </feed>
        """
        main.export(datetime(2020, 1, 1))
        assert open_mock.return_value.__enter__.return_value.write.call_count == 1
        assert "<apps:property name='from' value='@domain.com OR @email.domain.com'/>" in \
               open_mock.return_value.__enter__.return_value.write.call_args_list[0][0][0]
