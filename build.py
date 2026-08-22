#!/usr/bin/env python3
"""
Build script for SCU Cyber Security Knowledge Base.
Reads markdown articles from content/ and generates static HTML in dist/.

Usage: python build.py

Structure:
  content.json  — sections, categories (subcategories), and article metadata
  content/*.md  — article bodies with frontmatter
  templates/    — HTML templates
  assets/       — CSS, images
  dist/         — generated site (gitignored)
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
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', html)

    # Horizontal rule
    html = re.sub(r"^---$", r"<hr>", html, flags=re.MULTILINE)

    # Unordered lists
    def wrap_ul(match):
        items = re.findall(r"^- (.+)$", match.group(0), re.MULTILINE)
        wrapped = "<ul>\n"
        for item in items:
            wrapped += f"  <li>{item}</li>\n"
        wrapped += "</ul>"
        return wrapped

    html = re.sub(r"(?:^- .+\n?)+", wrap_ul, html, flags=re.MULTILINE)

    # Numbered lists
    def wrap_ol(match):
        items = re.findall(r"^\d+\. (.+)$", match.group(0), re.MULTILINE)
        wrapped = "<ol>\n"
        for item in items:
            wrapped += f"  <li>{item}</li>\n"
        wrapped += "</ol>"
        return wrapped

    html = re.sub(r"(?:^\d+\. .+\n?)+", wrap_ol, html, flags=re.MULTILINE)

    # Tables
    def wrap_table(match):
        lines = match.group(0).strip().split("\n")
        rows = []
        for line in lines:
            line = line.strip().strip("|")
            cells = [c.strip() for c in line.split("|")]
            rows.append(cells)

        if len(rows) < 2:
            return match.group(0)
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

    html = re.sub(
        r"(?:^\|.+\|\n)+(?:^\|[-: |]+\|\n)(?:^\|.+\|\n?)+",
        wrap_table,
        html,
        flags=re.MULTILINE,
    )

    # Paragraphs: wrap remaining text blocks in <p>
    paragraphs = []
    in_html = False
    html_buf = []
    for block in html.split("\n\n"):
        block = block.strip()
        if not block:
            continue

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

        if block.startswith("<") and block.endswith(">"):
            paragraphs.append(block)
            continue

        block_html = block.replace("\n", " ")
        paragraphs.append(f"<p>{block_html}</p>")

    result = "\n\n".join(paragraphs)

    # FAQ blocks → accordion
    def faq_to_accordion(match):
        inner = match.group(1).strip()
        parts = re.split(r'(?:\n\n)?(?:<p>)?<strong>', inner)
        result_html = ""
        idx = 0
        for part in parts:
            part = part.strip()
            if not part:
                continue
            end_q = part.find('</strong>')
            if end_q == -1:
                continue
            q = part[:end_q].strip()
            a_raw = part[end_q + len('</strong>'):].strip()
            if a_raw.startswith('</p>'):
                a_raw = a_raw[4:].strip()
            if a_raw and not a_raw.startswith('<'):
                a_raw = f'<p>{a_raw}</p>'
            a_raw = re.sub(r'<p>\s*</p>', '', a_raw)
            result_html += f"""
<div class="faq-item">
  <button class="faq-q" aria-expanded="false" aria-controls="faq-{idx}">{q}</button>
  <div class="faq-a" id="faq-{idx}" aria-hidden="true">
    {a_raw}
  </div>
</div>"""
            idx += 1
        return result_html

    result = re.sub(r'<div class="faq">(.*?)</div>', faq_to_accordion, result, flags=re.DOTALL)

    return result


def _meta_bar(fm):
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
    return "\n".join(meta_parts) if meta_parts else ""


def build_site():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ASSETS_DIR, DIST / "assets")

    config = load_json(ROOT / "content.json")
    articles = config["articles"]
    sections = config["sections"]
    categories = config["categories"]
    report_incident = config.get("report_incident", {})

    # Index articles by id
    by_id = {a["id"]: a for a in articles}

    # Group by section and category
    by_section = {s["id"]: [] for s in sections}
    for art in articles:
        by_section.setdefault(art["section"], []).append(art)

    cat_labels = {}
    for sec_id, cats in categories.items():
        for c in cats:
            cat_labels[c["id"]] = c["label"]

    section_labels = {s["id"]: s["label"] for s in sections}

    # ── Build article pages ──
    for art in articles:
        md_path = CONTENT_DIR / f"{art['id']}.md"
        if not md_path.exists():
            print(f"WARNING: Missing content file {md_path}")
            continue

        raw = md_path.read_text(encoding="utf-8")
        fm, body = parse_markdown(raw)
        body_html = markdown_to_html(body)

        title = art["title"]
        section = art["section"]
        section_label = section_labels.get(section, section)

        # Sidebar: other articles in same section, grouped by category
        sidebar = ""
        peers = sorted(by_section.get(section, []), key=lambda x: x.get("order", 99))
        if peers:
            # group by category
            grouped = {}
            for p in peers:
                cat = p.get("category")
                key = cat or ""
                grouped.setdefault(key, []).append(p)

            for cat_id, cat_arts in grouped.items():
                if cat_id and cat_id in cat_labels:
                    sidebar += f'<li class="sidebar-nav__heading">{cat_labels[cat_id]}</li>\n'
                for a in cat_arts:
                    cls = ' class="active"' if a["id"] == art["id"] else ""
                    sidebar += f'<li><a href="/{a["id"]}"{cls}>{a["title"]}</a></li>\n'

        variables = {
            "title": title,
            "description": art.get("description", ""),
            "section_label": section_label,
            "meta": _meta_bar(fm),
            "sidebar": sidebar,
            "body": body_html,
        }

        html = render_template(TEMPLATES_DIR / "article.html", variables)
        out_path = DIST / f"{art['id']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  Built: {out_path}")

    # ── Build index page ──
    index_html = build_index(sections, by_section, categories, cat_labels, report_incident)
    (DIST / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  Built: {DIST / 'index.html'}")

    # ── Build section landing pages ──
    for sec in sections:
        sec_id = sec["id"]
        sec_arts = sorted(by_section.get(sec_id, []), key=lambda x: x.get("order", 99))
        sec_html = build_section_page(sec, sec_arts, categories.get(sec_id, []), cat_labels)
        (DIST / f"{sec_id}.html").write_text(sec_html, encoding="utf-8")
        print(f"  Built: {DIST / f'{sec_id}.html'}")

    # ── 404 ──
    (DIST / "404.html").write_text(index_html, encoding="utf-8")
    print(f"  Built: {DIST / '404.html'}")

    print(f"\nDone. Site built to {DIST}")


def build_index(sections, by_section, categories, cat_labels, report_incident=None):
    with open(TEMPLATES_DIR / "base.html", "r", encoding="utf-8") as f:
        tpl = f.read()

    section_blocks = ""
    for sec in sections:
        sec_id = sec["id"]
        sec_arts = sorted(by_section.get(sec_id, []), key=lambda x: x.get("order", 99))
        sec_cats = categories.get(sec_id, [])

        if sec_id == "announcements":
            # Announcements: highlight cards
            items = ""
            for a in sec_arts:
                badge = ""
                if a.get("action_required"):
                    badge = f'<span class="badge badge--alert">{a["action_required"]}</span>'
                items += f"""
            <a href="/{a['id']}" class="announcement-card">
              <div class="announcement-card__badges">{badge}</div>
              <h3>{a['title']}</h3>
              <p>{a.get('description', '')}</p>
              <span class="announcement-card__action">Read more →</span>
            </a>"""
            section_blocks += f"""
      <section class="home-section">
        <h2 class="home-section__heading">{sec['label']}</h2>
        <div class="announcement-grid">{items}</div>
      </section>"""

        elif sec_id == "awareness":
            # Awareness: grid of cards
            items = ""
            for a in sec_arts:
                items += f"""
            <a href="/{a['id']}" class="awareness-card">
              <h3>{a['title']}</h3>
              <p>{a.get('description', '')}</p>
            </a>"""
            section_blocks += f"""
      <section class="home-section">
        <h2 class="home-section__heading">{sec['label']}</h2>
        <div class="awareness-grid">{items}</div>
      </section>"""

        else:
            # Knowledge base: compact card grid of categories (not full article list)
            grouped = {}
            for a in sec_arts:
                grouped.setdefault(a.get("category", ""), []).append(a)

            kb_html = '<div class="kb-card-grid">'
            for cat in sec_cats:
                cat_id = cat["id"]
                cat_arts = grouped.get(cat_id, [])
                if not cat_arts:
                    continue
                first = cat_arts[0]
                kb_html += f"""
            <a href="/knowledge-base#{cat_id}" class="kb-card">
              <h3>{cat['label']}</h3>
              <p>{first.get('description', '')}</p>
              <span class="kb-card__count">{len(cat_arts)} article{'s' if len(cat_arts) != 1 else ''}</span>
            </a>"""
            kb_html += "</div>"

            section_blocks += f"""
      <section class="home-section">
        <h2 class="home-section__heading">{sec['label']}</h2>
        {kb_html}
      </section>"""

    # ── Report a cyber incident section ──
    report_incident_html = ""
    if report_incident:
        bullets = "\n".join(f"""<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg><span>{item}</span></li>""" for item in report_incident.get("what_to_include", []))
        report_incident_html = f"""
      <section class="report-incident">
        <div class="report-incident__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.2 7.7-8 9-4.8-1.3-8-4.5-8-9V6l8-3z"/><path d="M12 9v4"/><path d="M12 16.5h.01"/></svg>
        </div>
        <div class="report-incident__text">
          <h2 class="report-incident__title">{report_incident.get('title', 'Report a cyber incident')}</h2>
          <p class="report-incident__intro">{report_incident.get('intro', '')}</p>
          <ul class="report-incident__list">
            {bullets}
          </ul>
        </div>
        <div class="report-incident__action">
          <a href="{report_incident.get('button_url', '#')}" class="report-incident__button" target="_blank" rel="noopener">{report_incident.get('button_label', 'Report an incident')} →</a>
        </div>
      </section>"""

    content = f"""
    <div class="page-wrapper">

      <section class="home-hero">
        <div class="home-hero__text">
          <p class="home-hero__eyebrow">Southern Cross University</p>
          <h1>Cyber Security</h1>
          <p class="home-hero__lede">Practical guidance, awareness materials, and how-to guides to help staff and students stay secure online.</p>
          <div class="home-hero__actions">
            <a href="/meet-lockie" class="home-hero__cta">Meet Lockie, your guide</a>
            <a href="/knowledge-base" class="home-hero__cta--ghost">Browse the knowledge base</a>
          </div>
        </div>
        <div class="home-hero__figure" aria-hidden="true">
          <img src="/assets/lockie.png" alt="" width="217" height="345">
        </div>
      </section>

      {section_blocks}

      {report_incident_html}

    </div>"""

    variables = {
        "title": "Cyber Security",
        "description": "Cyber security information and guides for SCU staff and students.",
        "section_label": "Home",
        "content": content,
    }
    return render_template(TEMPLATES_DIR / "base.html", variables)


def build_section_page(section, section_articles, section_categories, cat_labels):
    with open(TEMPLATES_DIR / "base.html", "r", encoding="utf-8") as f:
        tpl = f.read()

    label = section["label"]

    # Group articles by category, preserving category config order
    grouped = {}
    for a in section_articles:
        grouped.setdefault(a.get("category", ""), []).append(a)

    body = ""
    if section_articles:
        cat_order = [c["id"] for c in section_categories] if section_categories else list(grouped.keys())
        for cat_id in cat_order:
            cat_arts = grouped.get(cat_id)
            if not cat_arts:
                continue
            cat_label = cat_labels.get(cat_id, "Other")
            body += f'<h2 class="section-category-heading" id="{cat_id}">{cat_label}</h2>\n<ul class="article-list">\n'
            for a in cat_arts:
                body += f"""<li><a href="/{a['id']}">
              <span class="article-list__title">{a['title']}</span>
              <span class="article-list__desc">{a.get('description','')}</span>
            </a></li>"""
            body += "</ul>\n"
        # Uncategorized leftovers
        leftovers = [a for a in section_articles if not a.get("category") or a["category"] not in cat_order]
        if leftovers:
            body += '<h2 class="section-category-heading" id="other">Other</h2>\n<ul class="article-list">\n'
            for a in leftovers:
                body += f"""<li><a href="/{a['id']}">
              <span class="article-list__title">{a['title']}</span>
              <span class="article-list__desc">{a.get('description','')}</span>
            </a></li>"""
            body += "</ul>\n"
    else:
        body = "<p>Nothing here yet.</p>"

    content = f"""
    <div class="page-wrapper">
      <div class="page-banner">
        <h1>{label}</h1>
        <div class="page-banner__meta"><span>{len(section_articles)} article{'s' if len(section_articles) != 1 else ''}</span></div>
      </div>
      {body}
    </div>"""

    variables = {
        "title": label,
        "description": f"{label} — SCU Cyber Security",
        "section_label": label,
        "content": content,
    }
    return render_template(TEMPLATES_DIR / "base.html", variables)


if __name__ == "__main__":
    build_site()