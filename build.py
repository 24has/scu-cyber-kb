#!/usr/bin/env python3
"""
Build script for SCU Cyber Security Knowledge Base.
Reads markdown articles from content/ and generates static HTML in dist/.

Usage: python build.py

Edit the markdown files in content/ to update articles.
Add new articles to content.json to include them.
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
DIST = ROOT / "dist"

CATEGORY_LABELS = {
    "multi-factor-authentication": "Multi-factor authentication",
    "passwords": "Passwords",
    "phishing": "Phishing",
    "devices": "Devices",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_template(template_path, variables):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()

    for key, value in variables.items():
        tpl = tpl.replace("{{ " + key + " }}", value)

    return tpl


def parse_markdown(text):
    """Parse the frontmatter + markdown body."""
    fm = {}
    body = text

    # Frontmatter (+++ ... +++)
    if text.startswith("+++"):
        end = text.find("+++", 3)
        if end != -1:
            fm_text = text[3:end].strip()
            for line in fm_text.split("\n"):
                line = line.strip()
                if "=" in line:
                    key, _, val = line.partition("=")
                    fm[key.strip()] = val.strip().strip('"')
            body = text[end + 3 :].strip()

    return fm, body


def markdown_to_html(text):
    """Convert markdown body to HTML. Handles common patterns."""
    html = text

    # Headings
    html = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

    # Inline code
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # Links [text](url)
    html = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', html
    )

    # Horizontal rule
    html = re.sub(r"^---$", r"<hr>", html, flags=re.MULTILINE)

    # Unordered lists (lines starting with - )
    # We need to group contiguous - lines
    def wrap_ul(match):
        items = re.findall(r"^- (.+)$", match.group(0), re.MULTILINE)
        wrapped = "<ul>\n"
        for item in items:
            wrapped += f"  <li>{item}</li>\n"
        wrapped += "</ul>"
        return wrapped

    html = re.sub(r"(?:^- .+\n?)+", wrap_ul, html, flags=re.MULTILINE)

    # Tables: | col | col |
    def wrap_table(match):
        lines = match.group(0).strip().split("\n")
        rows = []
        for line in lines:
            line = line.strip().strip("|")
            cells = [c.strip() for c in line.split("|")]
            rows.append(cells)

        if len(rows) < 2:
            return match.group(0)

        # Skip separator row (---|---|---)
        data_rows = [r for r in rows if not all(re.match(r"^-+$", c) for c in r)]

        if len(data_rows) < 2:
            return match.group(0)

        header = data_rows[0]
        body_rows = data_rows[1:]

        out = '<table>\n<thead>\n<tr>\n'
        for cell in header:
            out += f"<th>{cell}</th>\n"
        out += "</tr>\n</thead>\n<tbody>\n"
        for row in body_rows:
            out += "<tr>\n"
            for cell in row:
                out += f"<td>{cell}</td>\n"
            out += "</tr>\n"
        out += "</tbody>\n</table>"
        return out

    # Match table blocks: lines with |col|col|... followed by |---|---|
    html = re.sub(
        r"(?:^\|.+\|\n)+(?:^\|[-: |]+\|\n)(?:^\|.+\|\n?)+",
        wrap_table,
        html,
        flags=re.MULTILINE,
    )

    # Paragraphs: wrap remaining text blocks in <p>
    # Split by double newlines
    paragraphs = []
    for block in html.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        # Skip blocks that are already HTML elements
        if block.startswith("<"):
            paragraphs.append(block)
        else:
            # Join single newlines within paragraph
            block_html = block.replace("\n", " ")
            paragraphs.append(f"<p>{block_html}</p>")

    return "\n\n".join(paragraphs)


def build_site():
    # Clean and recreate dist
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    # Copy assets
    shutil.copytree(ASSETS_DIR, DIST / "assets")

    # Load site config
    config = load_json(ROOT / "content.json")
    articles = config["articles"]
    nav = config["nav"]

    # Group articles by category
    by_category = {}
    for art in articles:
        cat = art["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(art)

    # Build article pages
    for art in articles:
        md_path = CONTENT_DIR / f"{art['id']}.md"
        if not md_path.exists():
            print(f"WARNING: Missing content file {md_path}")
            continue

        with open(md_path, "r", encoding="utf-8") as f:
            raw = f.read()

        fm, body = parse_markdown(raw)
        body_html = markdown_to_html(body)

        # Article metadata
        title = art["title"]
        category = art["category"]
        cat_label = CATEGORY_LABELS.get(category, category)

        # Meta bar
        meta_parts = []
        if fm.get("updated"):
            meta_parts.append(f"<span>Updated: {fm['updated']}</span>")
        if fm.get("applies_to"):
            meta_parts.append(f"<span>Applies to: {fm['applies_to']}</span>")
        if fm.get("time_required"):
            meta_parts.append(f"<span>🕐 {fm['time_required']}</span>")
        if fm.get("action_required"):
            meta_parts.append(
                f'<span class="badge badge--gold">Action required by {fm["action_required"]}</span>'
            )
        meta = "\n".join(meta_parts) if meta_parts else ""

        # Sidebar — other articles in same category
        sidebar = ""
        for a in sorted(by_category.get(category, []), key=lambda x: x.get("order", 99)):
            if a["id"] == art["id"]:
                sidebar += (
                    f'<li><a href="/{a["id"]}" class="active">{a["title"]}</a></li>\n'
                )
            else:
                sidebar += f'<li><a href="/{a["id"]}">{a["title"]}</a></li>\n'

        variables = {
            "title": title,
            "description": art.get("description", ""),
            "category_label": cat_label,
            "meta": meta,
            "sidebar": sidebar,
            "body": body_html,
        }

        html = render_template(TEMPLATES_DIR / "article.html", variables)
        out_path = DIST / f"{art['id']}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Built: {out_path}")

    # Build index page
    index_html = build_index(nav, by_category)
    with open(DIST / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  Built: {DIST / 'index.html'}")

    # Build 404
    with open(DIST / "404.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  Built: {DIST / '404.html'}")

    print(f"\nDone. Site built to {DIST}")


def build_index(nav, by_category):
    with open(TEMPLATES_DIR / "base.html", "r", encoding="utf-8") as f:
        tpl = f.read()

    # Build category cards
    cards = ""
    for item in nav:
        cat = item["category"]
        cat_articles = by_category.get(cat, [])
        count = len(cat_articles)
        label = CATEGORY_LABELS.get(cat, cat)

        if count == 0:
            cards += f"""
            <a href="#" class="category-card" style="opacity:.5">
              <h3>{label}</h3>
              <p>Coming soon</p>
              <div class="category-card__count">0 articles</div>
            </a>"""
        else:
            first_art = cat_articles[0]
            cards += f"""
            <a href="/{first_art['id']}" class="category-card">
              <h3>{label}</h3>
              <p>{item.get('label', '')}</p>
              <ul class="article-list" style="margin-top:1rem">
            """
            for art in sorted(cat_articles, key=lambda x: x.get("order", 99)):
                cards += f"""<li><a href="/{art['id']}">
                  <span class="article-list__title">{art['title']}</span>
                  <span class="article-list__desc">{art.get('description','')}</span>
                </a></li>"""
            cards += f"""
              </ul>
              <div class="category-card__count">{count} article{'s' if count != 1 else ''}</div>
            </a>"""

    content = f"""
    <div class="page-wrapper">
      <div class="home-hero">
        <h1>Cyber Security Knowledge Base</h1>
        <p>Information and step-by-step guides to help SCU staff and students stay secure online.</p>
      </div>

      <div class="category-grid">
        {cards}
      </div>
    </div>"""

    variables = {
        "title": "Cyber Security",
        "description": "Cyber security information and guides for SCU staff and students.",
        "category_label": "Home",
        "content": content,
    }

    for key, value in variables.items():
        tpl = tpl.replace("{{ " + key + " }}", value)

    return tpl


if __name__ == "__main__":
    build_site()