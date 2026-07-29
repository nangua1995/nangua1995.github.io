#!/usr/bin/env python3
"""Build search/timeline data and inject shared blog controls."""
import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def plain(value):
    value = re.sub(r"<script[\s\S]*?</script>", " ", value or "", flags=re.I)
    value = re.sub(r"<style[\s\S]*?</style>", " ", value, flags=re.I)
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    return re.sub(r"\s+", " ", value).strip()


def add_item(items, seen, path, title, date="", summary="", body="", tags=None, categories=None):
    if path in seen:
        return
    seen.add(path)
    items.append({
        "path": path, "title": title, "date": date,
        "summary": summary[:260], "text": plain(body)[:12000],
        "tags": tags or [], "categories": categories or [],
    })


def collect():
    items, seen = [], set()
    blog_manifest = ROOT / "blog" / "articles.json"
    if blog_manifest.exists():
        for item in json.loads(blog_manifest.read_text(encoding="utf-8"))["items"]:
            body = (ROOT / "blog" / "posts" / (item["slug"] + ".md")).read_text(encoding="utf-8")
            add_item(
                items, seen, "/article/" + item["slug"] + "/", item["title"],
                item["date"], item["summary"], body, item.get("tags", []), ["技术博客"],
            )
    wp_manifest = ROOT / "wordpress" / "posts.json"
    if wp_manifest.exists():
        for item in json.loads(wp_manifest.read_text(encoding="utf-8"))["items"]:
            body = (ROOT / "wordpress" / "posts" / ("wp-" + str(item["id"]) + ".html")).read_text(encoding="utf-8")
            add_item(
                items, seen, item["path"], item["title"], item["date"],
                plain(body)[:260], body, item.get("tags", []), item.get("categories", []),
            )
    for page in sorted((ROOT / "article").glob("*/index.html")):
        path = "/article/" + page.parent.name + "/"
        if path in seen:
            continue
        source = page.read_text(encoding="utf-8")
        title_match = re.search(r"<title>\s*([\s\S]*?)(?:\s*-\s*SnowCrane|\s*·\s*snowCrane)", source, re.I)
        date_match = re.search(r"(20\d{2}-\d{2}-\d{2})", source)
        title = plain(title_match.group(1)) if title_match else page.parent.name
        tags = [plain(tag) for tag in re.findall(r'href="/tags/#[^"]+"[^>]*>(.*?)</a>', source, re.I)]
        add_item(
            items, seen, path, title, date_match.group(1) if date_match else "",
            plain(source)[:260], source, tags, ["历史文章"],
        )
    items.sort(key=lambda x: (x["date"], x["title"]), reverse=True)
    return items


def timeline_page(items):
    years = defaultdict(list)
    for item in items:
        years[item["date"][:4] if item["date"] else "Earlier"].append(item)
    sections = []
    for year in sorted(years, reverse=True):
        rows = "".join(
            '<li><time>{}</time><a href="{}">{}</a></li>'.format(
                html.escape(item["date"][5:] if len(item["date"]) >= 10 else item["date"]),
                html.escape(item["path"], quote=True), html.escape(item["title"]),
            ) for item in years[year]
        )
        sections.append('<section><h2 class="timeline-year">{}</h2><ul class="timeline-list">{}</ul></section>'.format(year, rows))
    return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>文章时间轴 · snowCrane</title>
<link rel="stylesheet" href="/blog/static/style.css"></head><body>
<header class="hero"><div class="hero-inner"><a class="brand" href="/">snowCrane</a><nav><a href="/">文章</a></nav></div></header>
<main><div class="timeline"><h1>文章时间轴</h1><p>共 {} 篇归档文章</p>{}</div></main>
<footer>© snowCrane</footer></body></html>""".format(len(items), "".join(sections))


def inject(page):
    source = page.read_text(encoding="utf-8")
    css = '<link rel="stylesheet" href="/css/snowcrane-features.css">'
    script = '<script defer src="/js/snowcrane-features.js"></script>'
    if css not in source:
        source = source.replace("</head>", css + "\n</head>", 1)
    if script not in source:
        source = source.replace("</body>", script + "\n</body>", 1)
    page.write_text(source, encoding="utf-8")


def main():
    items = collect()
    (ROOT / "search-index.json").write_text(
        json.dumps({"items": items}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (ROOT / "archive-index.json").write_text(
        json.dumps({"items": items}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    timeline = ROOT / "timeline"
    timeline.mkdir(exist_ok=True)
    (timeline / "index.html").write_text(timeline_page(items), encoding="utf-8")
    pages = [ROOT / "index.html", timeline / "index.html"]
    pages.extend((ROOT / "article").glob("*/index.html"))
    for page in pages:
        inject(page)
    print("built features for {} articles and {} pages".format(len(items), len(pages)))


if __name__ == "__main__":
    main()
