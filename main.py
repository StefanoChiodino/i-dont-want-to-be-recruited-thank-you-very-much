import argparse
import os
import re
import sys
from datetime import datetime
from re import Pattern
from typing import List, Dict, Any, TypeVar, Generator

# https://regex101.com/r/sbHlJ5/2.
from jinja2 import Template

_DOMAIN_REGEX: str = r"^[^:\/@]+\.[^:\/@]+$"
_FILE_PATH: str = "domains.txt"
_GMAIL_FILTER_TEMPLATE_PATH: str = "gmail_template.jinja2"
_GMAIL_FILTER_PATH: str = "gmail_filter.xml"
_TITLE: str = "I don't want to be recruited thank you very much"
X: TypeVar = TypeVar('X')


def argparser_domain_type(arg_value: str, pat: Pattern = re.compile(_DOMAIN_REGEX)) -> str:
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError(f"'{arg_value}' is not a valid domain!")
    return arg_value


def _get_all_domains() -> List[str]:
    try:
        with open(_FILE_PATH, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def add(domain: str):
    domains: List[str] = _get_all_domains()
    print(domains)
    domains.append(domain)
    # Dedupe.
    domains = list(set(domains))
    domains.sort(key=lambda x: x.lower())

    print(domains)
    with open(_FILE_PATH, "w") as file:
        file.write(os.linesep.join(domains))


def remove(domain: str):
    domains: List[str] = _get_all_domains()
    domains.remove(domain)
    domains.sort()
    with open(_FILE_PATH, "rw") as file:
        file.writelines(domains)




def _chunk_list(domains: List[X], chunk_size: int = 70) -> Generator[List[X], None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(domains), chunk_size):
        yield domains[i:i + chunk_size]


def export(as_at: datetime = None) -> None:
    domains: List[str] = _get_all_domains()
    if as_at is None:
        as_at = datetime.now()

    def get_entries() -> Generator[Dict[str, Any], None, None]:
        chunked_domains = _chunk_list(domains)
        for chunk in chunked_domains:
            yield {
                "title": _TITLE,
                "updated": as_at,
                "from": " OR ".join([f"@{x}" for x in chunk])
            }

    payload: Dict[str, Any] = {
        "title": _TITLE,
        "updated": as_at,
        "author": {
            "name": "Stefano Chiodino",
            "email": ""
        },
        "entries": get_entries()
    }

    with open(_GMAIL_FILTER_TEMPLATE_PATH, "r") as file:
        template_as_str: str = file.read()

    template: Template = Template(template_as_str)
    output = template.render(payload)

    with open(_GMAIL_FILTER_PATH, "w") as file:
        file.write(output)


def _parse_args(arguments: List[str]) -> argparse.Namespace:
    argparser = argparse.ArgumentParser()
    subparser = argparser.add_subparsers(dest="action")

    add_parser = subparser.add_parser("add")
    add_parser.add_argument("domain", type=argparser_domain_type)

    remove_parser = subparser.add_parser("remove")
    remove_parser.add_argument("domain", type=argparser_domain_type)

    subparser.add_parser("export")

    return argparser.parse_args(arguments)


if __name__ == '__main__':
    args = _parse_args(sys.argv[1:])

    if args.action == "add":
        add(args.domain)
    elif args.action == "remove":
        remove(args.domain)
    elif args.action == "export":
        export()
