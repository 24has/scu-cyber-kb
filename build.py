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
    "announcements": "Announcements",
    "awareness": "Awareness",
    "knowledge-base": "Knowledge Base",
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
    # Split by double newlines, preserving HTML blocks
    paragraphs = []
    in_html = False
    html_buf = []
    for block in html.split("\n\n"):
        block = block.strip()
        if not block:
            continue

        # Track multi-line HTML open/close divs
        is_open = block.startswith("<div") and not block.endswith(">")
        is_close = block == "</div>"

        if is_open:
            in_html = True
            html_buf.append(block)
            continue

        if in_html:
            html_buf.append(block)
            if is_close:
                paragraphs.append("\n\n".join(html_buf))
                html_buf = []
                in_html = False
            continue

        # Single-line HTML tags pass through
        if block.startswith("<") and block.endswith(">"):
            paragraphs.append(block)
            continue

        # Join single newlines within paragraph, wrap in <p>
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

    def article_items(arts):
        items = ""
        for a in sorted(arts, key=lambda x: x.get("order", 99)):
            items += f"""<li><a href="/{a['id']}">
              <span class="article-list__title">{a['title']}</span>
              <span class="article-list__desc">{a.get('description','')}</span>
            </a></li>"""
        return items

    # ── Announcements section ──
    announcements = by_category.get("announcements", [])
    announcements_html = ""
    if announcements:
        for a in sorted(announcements, key=lambda x: x.get("order", 99)):
            badges = ""
            if a.get("action_required"):
                badges += f'<span class="badge badge--alert">{a["action_required"]}</span>'
            announcements_html += f"""
            <a href="/{a['id']}" class="announcement-card">
              <div class="announcement-card__badges">{badges}</div>
              <h3>{a['title']}</h3>
              <p>{a.get('description', '')}</p>
              <span class="announcement-card__action">Read more →</span>
            </a>"""

    # ── Awareness section ──
    awareness = by_category.get("awareness", [])
    awareness_html = ""
    if awareness:
        for a in sorted(awareness, key=lambda x: x.get("order", 99)):
            awareness_html += f"""
            <a href="/{a['id']}" class="awareness-card">
              <h3>{a['title']}</h3>
              <p>{a.get('description', '')}</p>
            </a>"""

    # ── Knowledge Base section ──
    kb = by_category.get("knowledge-base", [])
    kb_html = ""
    if kb:
        kb_articles = sorted(kb, key=lambda x: x.get("order", 99))
        kb_html = f'<ul class="article-list">\n{article_items(kb_articles)}</ul>'

    content = f"""
    <div class="page-wrapper">

      <div class="home-hero">
        <h1>Cyber Security</h1>
        <p>Information, awareness, and step-by-step guides to help SCU staff and students stay secure.</p>
      </div>

      <!-- ═══ ANNOUNCEMENTS ═══ -->
      <section class="home-section">
        <h2 class="home-section__heading">Announcements</h2>
        <div class="announcement-grid">
          {announcements_html}
        </div>
      </section>

      <!-- ═══ AWARENESS ═══ -->
      <section class="home-section">
        <h2 class="home-section__heading">Awareness</h2>
        <div class="awareness-grid">
          {awareness_html}
        </div>
      </section>

      <!-- ═══ KNOWLEDGE BASE ═══ -->
      <section class="home-section">
        <h2 class="home-section__heading">Knowledge Base</h2>
        {kb_html}
      </section>

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