#!/usr/bin/env python3
"""Собирает privacy.html и terms.html из текстов приложения
(../../App/NetStatus/Legal/*.md) — один источник для экрана и сайта.
Запуск: python3 build_legal.py"""
import html, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent
LEGAL = SITE.parent.parent / "App" / "NetStatus" / "Legal"
DOCS = {"privacy": "Clarity — Privacy Policy", "terms": "Clarity — Terms of Service"}
LINKS = {"privacy": "privacy.html", "terms": "terms.html"}

def inline(text: str) -> str:
    out, i = [], 0
    while i < len(text):
        if text.startswith("__", i):
            j = text.find("__", i + 2)
            if j > 0:
                out.append("<dfn>" + html.escape(text[i + 2:j]) + "</dfn>"); i = j + 2; continue
        if text.startswith("[[", i):
            j = text.find("]]", i)
            if j > 0:
                out.append('<span class="placeholder">[' + html.escape(text[i + 2:j]) + "]</span>"); i = j + 2; continue
        m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", text[i:])
        if m:
            target = m.group(2)
            href = target if ":" in target else LINKS.get(target, target)
            out.append(f'<a href="{html.escape(href)}">{html.escape(m.group(1))}</a>'); i += m.end(); continue
        out.append(html.escape(text[i])); i += 1
    return "".join(out)

def parse(text: str):
    meta = {"title": "", "kicker": "", "updated": ""}
    blocks, para, bullets = [], [], []
    def flush():
        nonlocal para, bullets
        if para: blocks.append(("p", " ".join(para))); para = []
        if bullets: blocks.append(("ul", bullets)); bullets = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line: flush(); continue
        if line.startswith("# "): meta["title"] = line[2:]; continue
        if line.startswith("Kicker: "): meta["kicker"] = line[8:]; continue
        if line.startswith("Updated: "): meta["updated"] = line[9:]; continue
        if line.startswith("## "): flush(); blocks.append(("h2", line[3:])); continue
        if line.startswith("- "):
            if para: flush()
            bullets.append(line[2:]); continue
        if bullets: flush()
        para.append(line)
    flush()
    return meta, blocks

def render_blocks(blocks):
    parts = []
    for kind, value in blocks:
        if kind == "h2": parts.append(f"<h2>{html.escape(value)}</h2>\n")
        elif kind == "p": parts.append(f"<p>{inline(value)}</p>\n")
        else: parts.append("<ul>\n" + "".join(f"  <li>{inline(v)}</li>\n" for v in value) + "</ul>\n")
    return "\n".join(parts)

def head(meta, langs=False):
    extra = '  <p class="langs"><a href="#en">English</a><a href="#ru">Русский</a></p>\n' if langs else ""
    return (f'<header class="doc-head">\n  <p class="kicker">{html.escape(meta["kicker"])}</p>\n'
            f'  <h1>{html.escape(meta["title"])}</h1>\n  <p class="updated">{html.escape(meta["updated"])}</p>\n{extra}</header>\n')

for doc, page_title in DOCS.items():
    en_meta, en_blocks = parse((LEGAL / f"{doc}.en.md").read_text())
    ru_meta, ru_blocks = parse((LEGAL / f"{doc}.ru.md").read_text())
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

{head(en_meta, langs=True)}
<main id="en">

{render_blocks(en_blocks)}
</main>

<main id="ru" lang="ru">

{head(ru_meta)}
{render_blocks(ru_blocks)}
</main>

<footer>
  <p><a href="./">Support</a><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a></p>
  <p>© 2026 Matchy Labs LTD</p>
</footer>

</body>
</html>
"""
    (SITE / f"{doc}.html").write_text(page)
    print("wrote", doc + ".html")
