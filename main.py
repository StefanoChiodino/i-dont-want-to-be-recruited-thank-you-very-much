import argparse
import os
import re
import sys
from datetime import datetime
from re import Pattern
from typing import List, Dict, Callable, Any

# https://regex101.com/r/sbHlJ5/2.
from jinja2 import Template
from setuptools._vendor.ordered_set import OrderedSet

_DOMAIN_REGEX = r"^[^:\/@]+\.[^:\/@]+$"
_FILE_PATH = "domains.txt"
_GMAIL_FILTER_TEMPLATE_PATH = "gmail_template.jinja2"
_GMAIL_FILTER_PATH = "gmail_filter.xml"


def argparser_domain_type(arg_value: str, pat: Pattern = re.compile(_DOMAIN_REGEX)) -> str:
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError(f"'{arg_value}' is not a valid domain!")
    return arg_value


def _get_all_domains() -> List[str]:
    try:
        with open(_FILE_PATH, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def add(domain: str):
    domains: List[str] = _get_all_domains()
    domains.append(domain + os.linesep)
    domains.sort(key=lambda x: x.lower())
    unique_domains = OrderedSet(domains)
    print(unique_domains)
    with open(_FILE_PATH, "w") as file:
        file.writelines(unique_domains)


def remove(domain: str):
    domains: List[str] = _get_all_domains()
    domains.remove(domain)
    domains.sort()
    with open(_FILE_PATH, "rw") as file:
        file.writelines(domains)


def export(as_at: datetime = None) -> None:
    domains: List[str] = _get_all_domains()
    if as_at is None:
        as_at = datetime.now()
    filter: Dict[str, Any] = {
        "title": "I don't want to be recruited thanks",
        "updated": as_at,
        "author": {
            "name": "I don't want to be recruited thanks",
            "email": ""
        },
        "entries": [
            {
                "title": "I don't want to be recruited thanks",
                "updated": as_at,
                "from": " OR ".join([f"@{x}" for x in domains])
            }
        ]
    }

    with open(_GMAIL_FILTER_TEMPLATE_PATH, "r") as file:
        template_as_str: str = file.read()

    template: Template = Template(template_as_str)
    output = template.render(filter)

    with open(_GMAIL_FILTER_PATH, "w") as file:
        file.write(output)


# Press the green button in the gutter to run the script.
def _parse_args(args: List[str]) -> argparse.Namespace:
    argparser = argparse.ArgumentParser()
    subparser = argparser.add_subparsers(dest="action")

    add_parser = subparser.add_parser("add")
    add_parser.add_argument("domain", type=argparser_domain_type)

    remove_parser = subparser.add_parser("remove")
    remove_parser.add_argument("domain", type=argparser_domain_type)

    export_parser = subparser.add_parser("export")

    return argparser.parse_args(args)


if __name__ == '__main__':
    args = _parse_args(sys.argv[1:])
    # sourcecoders.io
    print(args)

    if args.action == "add":
        add(args.domain)
    elif args.action == "remove":
        remove(args.domain)
    elif args.action == "export":
        export()
