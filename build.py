#!/usr/bin/env python3
"""
foid-report — a tiny static generator for foid.report. No dependencies.
Reads markdown files from posts/ and writes a static site to docs/.
Run it with:  python3 build.py

How posting works:
  - Make a file in posts/ named by date, e.g.  posts/2026-07-01.md
  - (Optional) open with a frontmatter block:

        ---
        title: the report title
        ---

    No frontmatter is fine too — a lone "# Title" first line still works,
    and a bare paragraph is a valid entry (it gets the date as its title).
  - Run this script. The docs/ folder is the finished website.

Multiple posts in one day? Add a suffix:  posts/2026-07-01-two.md
"""

import html
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
SITE_DIR = ROOT / "docs"  # GitHub Pages serves from /docs on the main branch
STYLE_SRC = ROOT / "style.css"

SITE_TITLE = "FOID REPORT"
DOMAIN = "foid.report"


# ----------------------------- markdown ------------------------------------ #
# A deliberately small markdown subset that covers blog prose: headings,
# paragraphs, bold/italic, links, inline code, blockquotes, lists, rules.

_INLINE_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
_ITALIC = re.compile(r"(?<![*_])\*(?!\s)([^*]+?)\*(?![*])|(?<![*_])_(?!\s)([^_]+?)_(?![_])")


def _inline(text: str) -> str:
    text = html.escape(text, quote=False)
    codes: list[str] = []

    def stash(m: "re.Match[str]") -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = _INLINE_CODE.sub(stash, text)
    text = _LINK.sub(r'<a href="\2">\1</a>', text)
    text = _BOLD.sub(lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = _ITALIC.sub(lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", text)
    return text


def md_to_html(src: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_para(buf: list[str]) -> None:
        if buf:
            out.append(f"<p>{_inline(' '.join(l.strip() for l in buf))}</p>")
            buf.clear()

    para: list[str] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para(para)
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_para(para)
            level = min(len(m.group(1)) + 1, 5)  # h1 in a post renders as h2
            out.append(f"<h{level}>{_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para(para)
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote><p>{_inline(' '.join(quote))}</p></blockquote>")
            continue

        if re.match(r"^[-*+]\s+", stripped):
            flush_para(para)
            items: list[str] = []
            while i < n and re.match(r"^[-*+]\s+", lines[i].strip()):
                items.append(f"<li>{_inline(re.sub(r'^[-*+]\\s+', '', lines[i].strip()))}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            flush_para(para)
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(f"<li>{_inline(re.sub(r'^\\d+\\.\\s+', '', lines[i].strip()))}</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        para.append(line)
        i += 1

    flush_para(para)
    return "\n".join(out)


# ------------------------------ posts -------------------------------------- #

_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_DATE_IN_NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")


def parse_post(path: Path) -> dict | None:
    m = _DATE_IN_NAME.match(path.stem)
    if not m:
        return None
    post_date = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    src = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    fm = _FRONTMATTER.match(src)
    if fm:
        for line in fm.group(1).splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip().lower()] = val.strip()
        src = src[fm.end():]

    body = src.strip()
    title = meta.get("title", "")
    if not title:
        first = body.split("\n", 1)[0].strip()
        if first.startswith("#"):
            title = first.lstrip("#").strip()
            body = body.split("\n", 1)[1].strip() if "\n" in body else ""
    if not title:
        title = post_date.strftime("%B %-d, %Y").lower()

    return {
        "slug": path.stem,
        "date": post_date,
        "title": title,
        "html": md_to_html(body),
    }


# ------------------------------ pages -------------------------------------- #

def page(title: str, body: str, depth: int = 0) -> str:
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<header class="masthead"><a href="{prefix}index.html">{html.escape(SITE_TITLE)}</a></header>
<main>
{body}
</main>
<footer>{html.escape(DOMAIN)}</footer>
</body>
</html>
"""


def post_article(post: dict, heading_link: str | None = None) -> str:
    title = html.escape(post["title"])
    heading = f'<a href="{heading_link}">{title}</a>' if heading_link else title
    stamp = post["date"].strftime("%B %-d, %Y").lower()
    return (
        '<article class="post">\n'
        f"<h2>{heading}</h2>\n"
        f'<p class="stamp">{stamp}</p>\n'
        f"{post['html']}\n"
        "</article>"
    )


def build() -> None:
    posts = sorted(
        filter(None, (parse_post(p) for p in POSTS_DIR.glob("*.md"))),
        key=lambda p: (p["date"], p["slug"]),
        reverse=True,
    )

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    (SITE_DIR / "posts").mkdir(parents=True)

    shutil.copy(STYLE_SRC, SITE_DIR / "style.css")
    (SITE_DIR / "CNAME").write_text(DOMAIN + "\n")

    if posts:
        feed = "\n".join(post_article(p, f"posts/{p['slug']}.html") for p in posts)
    else:
        feed = '<p class="stamp">no reports yet.</p>'
    (SITE_DIR / "index.html").write_text(page(SITE_TITLE, feed), encoding="utf-8")

    for p in posts:
        (SITE_DIR / "posts" / f"{p['slug']}.html").write_text(
            page(f"{p['title']} — {SITE_TITLE}", post_article(p), depth=1),
            encoding="utf-8",
        )

    print(f"built {len(posts)} post(s) → {SITE_DIR}")


if __name__ == "__main__":
    build()
