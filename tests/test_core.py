from readmine.core import extract_article, to_markdown


def test_extract_article():
    title, body = extract_article("<title>T</title><nav>x</nav><p>Hello world</p><script>bad()</script>")
    assert title == "T"
    assert "Hello world" in body
    assert "bad" not in body
    assert to_markdown(title, body).startswith("# T")
