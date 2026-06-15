"""Static integrity checks for the Ananda AI frontend."""

from __future__ import annotations

import subprocess
import tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.scripts: list[str] = []
        self._inside_script = False
        self._script_parts: list[str] = []
        self.has_title = False
        self.has_viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if element_id := attributes.get("id"):
            self.ids.append(element_id)
        if tag in {"a", "link"} and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag in {"img", "script"} and attributes.get("src"):
            self.links.append(attributes["src"])
        if tag == "script" and not attributes.get("src"):
            self._inside_script = True
            self._script_parts = []
        if tag == "meta" and attributes.get("name") == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.has_title = True

    def handle_data(self, data: str) -> None:
        if self._inside_script:
            self._script_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside_script:
            self.scripts.append("".join(self._script_parts))
            self._inside_script = False


def resolve_local_link(page: Path, link: str) -> Path | None:
    parsed = urlparse(link)
    if parsed.scheme or parsed.netloc or link.startswith(('#', 'mailto:', 'tel:')):
        return None

    path = parsed.path
    if not path:
        return None
    candidate = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/"):
        candidate /= "index.html"
    return candidate.resolve()


def check_javascript(page: Path, scripts: list[str], errors: list[str]) -> None:
    for index, script in enumerate(scripts, start=1):
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as file:
            file.write(script)
            file.flush()
            result = subprocess.run(
                ["node", "--check", file.name],
                capture_output=True,
                text=True,
                check=False,
            )
        if result.returncode:
            errors.append(f"{page.relative_to(ROOT)} script {index}: {result.stderr.strip()}")


def main() -> int:
    errors: list[str] = []
    html_files = sorted(ROOT.glob("**/*.html"))

    if any(path.is_file() for path in (ROOT / "var" / "www").glob("**/*")):
        errors.append("deployment copies under var/www must not be committed")

    for page in html_files:
        parser = SiteParser()
        parser.feed(page.read_text(encoding="utf-8"))

        if not parser.has_title:
            errors.append(f"{page.relative_to(ROOT)}: missing <title>")
        if not parser.has_viewport:
            errors.append(f"{page.relative_to(ROOT)}: missing viewport metadata")

        for element_id, count in Counter(parser.ids).items():
            if count > 1:
                errors.append(f"{page.relative_to(ROOT)}: duplicate id '{element_id}'")

        for link in parser.links:
            target = resolve_local_link(page, link)
            if target is not None and not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: broken local link '{link}'")

        check_javascript(page, parser.scripts, errors)

    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Site checks passed for {len(html_files)} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
