#!/usr/bin/env python3
"""Mirror published WordPress posts into the legacy GitHub Pages article list."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://zhinengzuocang.cn"
API = ORIGIN + "/wp-json/wp/v2/posts"
OUT = ROOT / "wordpress"
EXCLUDED_IDS = {
    101, 137, 138, 188, 193, 197, 206, 216, 225, 238, 245,
    250, 258, 268, 273, 277, 280, 290, 298, 304, 311,
    909, 910, 911,
}
# 909–911 are already mirrored from Markdown. The other IDs are intentionally
# hidden from this archive and must stay excluded during future daily syncs.


def fetch_posts():
    query = urlencode({
        "status": "publish", "per_page": 100, "_embed": 1,
        "orderby": "date", "order": "desc",
    })
    with urlopen(API + "?" + query, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", value).strip()


def absolutize(content):
    content = content.replace('="/wp-content/', '="' + ORIGIN + "/wp-content/")
    content = content.replace("='/wp-content/", "='" + ORIGIN + "/wp-content/")
    content = content.replace('="/wp-json/', '="' + ORIGIN + "/wp-json/")
    return content


def article_page(post, content):
    title = text(post["title"]["rendered"])
    excerpt = text(post["excerpt"]["rendered"])
    date = post["date"][:10]
    source = post["link"]
    return """<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · snowCrane</title>
<link rel="stylesheet" href="/blog/static/style.css">
<link rel="stylesheet" href="/wordpress/static/wordpress.css">
</head><body>
<header class="hero"><div class="hero-inner"><a class="brand" href="/">snowCrane</a>
<nav><a href="/">文章</a><a href="/blog/">双语文章</a>
<a href="https://zhinengzuocang.cn/cockpit/">招聘雷达</a></nav></div></header>
<main><article class="wp-article">
<p class="back"><a href="/">← 返回文章列表</a></p>
<p class="meta">{date} · WordPress 归档</p>
<h1>{title}</h1><p class="summary">{excerpt}</p>
<div class="source-link"><a href="{source}">查看主站原文 ↗</a></div>
<div class="wp-content">{content}</div>
</article></main>
<footer>© snowCrane · GitHub Pages archive</footer>
</body></html>""".format(
        title=html.escape(title), excerpt=html.escape(excerpt), date=date,
        source=html.escape(source, quote=True), content=content,
    )


def main():
    posts = [post for post in fetch_posts() if post["id"] not in EXCLUDED_IDS]
    (OUT / "posts").mkdir(parents=True, exist_ok=True)
    (OUT / "static").mkdir(parents=True, exist_ok=True)
    cards, manifest = [], []
    for post in posts:
        post_id = int(post["id"])
        slug = "wp-" + str(post_id)
        title = text(post["title"]["rendered"])
        excerpt = text(post["excerpt"]["rendered"])
        if not excerpt:
            excerpt = text(post["content"]["rendered"])[:180]
        content = absolutize(post["content"]["rendered"])
        terms = [
            term for group in post.get("_embedded", {}).get("wp:term", [])
            for term in group
        ]
        categories = [term["name"] for term in terms if term.get("taxonomy") == "category"]
        tags = [term["name"] for term in terms if term.get("taxonomy") == "post_tag"]
        (OUT / "posts" / (slug + ".html")).write_text(content, encoding="utf-8")
        article_dir = ROOT / "article" / slug
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "index.html").write_text(
            article_page(post, content), encoding="utf-8",
        )
        cards.append("""<div class="post-preview">
<a href="/article/{slug}/"><h2 class="post-title">{title}</h2>
<h3 class="post-subtitle">{excerpt}</h3>
<div class="post-content-preview">{excerpt}</div></a>
<p class="post-meta" style="margin:10px 0;">Posted by SnowCrane on {date}</p>
</div><hr>""".format(
            slug=slug, title=html.escape(title), excerpt=html.escape(excerpt),
            date=post["date"][:10],
        ))
        manifest.append({
            "id": post_id, "path": "/article/" + slug + "/",
            "title": title, "date": post["date"][:10], "source": post["link"],
            "categories": categories, "tags": tags,
        })
    (OUT / "posts.json").write_text(
        json.dumps({"source": ORIGIN, "items": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    homepage = ROOT / "index.html"
    homepage_html = homepage.read_text(encoding="utf-8")
    start_marker = "<!-- WORDPRESS-MIRROR-START -->"
    end_marker = "<!-- WORDPRESS-MIRROR-END -->"
    block = start_marker + "\n" + "\n".join(cards) + "\n" + end_marker
    if start_marker in homepage_html:
        homepage_html = re.sub(
            re.escape(start_marker) + r"[\s\S]*?" + re.escape(end_marker),
            block, homepage_html, count=1,
        )
    else:
        server_end = "<!-- SERVER-BLOG-END -->"
        homepage_html = homepage_html.replace(server_end, server_end + "\n\n" + block, 1)
    homepage.write_text(homepage_html, encoding="utf-8")
    print("synced {} WordPress articles".format(len(posts)))


if __name__ == "__main__":
    main()
