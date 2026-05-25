from __future__ import annotations

import argparse
import sys
from .core import extract_article, to_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert accessible HTML to offline Markdown.")
    parser.add_argument("--url", default="")
    args = parser.parse_args(argv)
    title, body = extract_article(sys.stdin.read())
    print(to_markdown(title, body, args.url))
    return 0
