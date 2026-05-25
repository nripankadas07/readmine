from __future__ import annotations

import re
from html.parser import HTMLParser


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self._skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag == "title":
            self._in_title = True
        if tag in {"script", "style", "nav", "footer"}:
            self._skip += 1

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False
        if tag in {"script", "style", "nav", "footer"} and self._skip:
            self._skip -= 1

    def handle_data(self, data: str):
        text = " ".join(data.split())
        if not text:
            return
        if self._in_title:
            self.title += text
        elif not self._skip:
            self.parts.append(text)


def extract_article(html_text: str) -> tuple[str, str]:
    parser = ArticleParser()
    parser.feed(html_text)
    body = "\n\n".join(parser.parts)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return parser.title.strip() or "Untitled", body


def to_markdown(title: str, body: str, source_url: str = "") -> str:
    header = f"# {title}\n"
    if source_url:
        header += f"\nSource: {source_url}\n"
    return f"{header}\n{body}\n"
