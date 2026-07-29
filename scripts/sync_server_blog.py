#!/usr/bin/env python3
"""Mirror the public snowCrane Flask blog into this GitHub Pages repository."""
import html
import json
import re
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "blog"
ORIGIN = "https://zhinengzuocang.cn/blog"


def fetch_json(path):
    with urlopen(ORIGIN + path, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_bytes(path):
    with urlopen(ORIGIN + path, timeout=30) as response:
        return response.read()


def safe_slug(value):
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise ValueError("unsafe slug: " + value)
    return value


def attr(value):
    return html.escape(str(value), quote=True)


def shell(title, body, depth="", en_title=None):
    return """<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · snowCrane</title>
<link rel="stylesheet" href="{depth}static/style.css">
<script src="https://cdn.jsdelivr.net/npm/marked@13/marked.min.js"></script>
</head><body data-title-zh="{title_attr}" data-title-en="{en_title_attr}">
<header class="hero"><div class="hero-inner"><a class="brand" href="{depth}">snowCrane</a>
<nav><a href="{depth}" data-zh="文章" data-en="Articles">文章</a>
<a href="https://zhinengzuocang.cn/cockpit/" data-zh="招聘雷达" data-en="Talent Radar">招聘雷达</a>
<a href="https://github.com/nangua1995">GitHub</a>
<button type="button" id="langToggle">EN</button></nav></div></header>
<main>{body}</main><footer data-zh="© snowCrane · GitHub Pages 静态镜像" data-en="© snowCrane · GitHub Pages mirror">© snowCrane · GitHub Pages 静态镜像</footer>
<script>
(function(){{
  function apply(lang){{
    document.documentElement.lang=lang==="en"?"en":"zh-CN";
    document.querySelectorAll("[data-zh][data-en]").forEach(function(el){{el.textContent=el.dataset[lang];}});
    document.title=document.body.dataset["title"+(lang==="en"?"En":"Zh")]+" · snowCrane";
    document.getElementById("langToggle").textContent=lang==="en"?"中文":"EN";
    if(window.setArticleLanguage) window.setArticleLanguage(lang);
    localStorage.setItem("snowcrane-lang",lang);
  }}
  document.getElementById("langToggle").onclick=function(){{
    apply(document.documentElement.lang==="en"?"zh":"en");
  }};
  apply(localStorage.getItem("snowcrane-lang")==="en"?"en":"zh");
}})();
</script>
</body></html>""".format(
        title=html.escape(title), body=body, depth=depth,
        title_attr=attr(title), en_title_attr=attr(en_title or title),
    )


def main():
    items = fetch_json("/api/posts")["items"]
    (OUT / "posts").mkdir(parents=True, exist_ok=True)
    (OUT / "post").mkdir(parents=True, exist_ok=True)
    (OUT / "static").mkdir(parents=True, exist_ok=True)
    translation_path = OUT / "translations.en.json"
    translations = json.loads(translation_path.read_text(encoding="utf-8")) if translation_path.exists() else {}
    cards = []
    manifest = []
    for meta in items:
        slug = safe_slug(meta["slug"])
        full = fetch_json("/api/posts/" + slug)
        markdown = full.get("body", "")
        english = translations.get(slug, {})
        english_path = OUT / "posts" / (slug + ".en.md")
        remote_english = fetch_json("/api/posts/" + slug + "?lang=en")
        if (
            remote_english.get("translation_status") == "translated"
            and remote_english.get("body")
            and remote_english["body"] != markdown
        ):
            english_path.write_text(remote_english["body"], encoding="utf-8")
            english = {
                "title": remote_english.get("title", full.get("title", slug)),
                "summary": remote_english.get("summary", full.get("summary", "")),
                "tags": remote_english.get("tags", full.get("tags", [])),
            }
            translations[slug] = english
        english_markdown = english_path.read_text(encoding="utf-8") if english_path.exists() else markdown
        (OUT / "posts" / (slug + ".md")).write_text(markdown, encoding="utf-8")
        article_dir = OUT / "post" / slug
        article_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(markdown, ensure_ascii=False).replace("</", "<\\/")
        payload_en = json.dumps(english_markdown, ensure_ascii=False).replace("</", "<\\/")
        tags = " ".join("#" + html.escape(x) for x in full.get("tags", []))
        tags_en = " ".join("#" + html.escape(x) for x in english.get("tags", full.get("tags", [])))
        body = """<article>
<p class="back"><a href="../../" data-zh="← 返回文章列表" data-en="← Back to articles">← 返回文章列表</a></p>
<p class="meta">{date} · {reading_time} min read</p>
<h1 data-zh="{title_attr}" data-en="{title_en_attr}">{title}</h1>
<p class="summary" data-zh="{summary_attr}" data-en="{summary_en_attr}">{summary}</p>
<p class="tags" data-zh="{tags_attr}" data-en="{tags_en_attr}">{tags}</p>
<div id="content" class="markdown"></div>
<script type="application/json" id="sourceZh">{payload}</script>
<script type="application/json" id="sourceEn">{payload_en}</script>
<script>window.setArticleLanguage=function(lang){{var id=lang==="en"?"sourceEn":"sourceZh";document.getElementById("content").innerHTML=marked.parse(JSON.parse(document.getElementById(id).textContent));}};</script>
</article>""".format(
            date=html.escape(str(full.get("date", ""))),
            reading_time=html.escape(str(full.get("reading_time", ""))),
            title=html.escape(full.get("title", slug)),
            summary=html.escape(full.get("summary", "")),
            tags=tags, payload=payload, payload_en=payload_en,
            title_attr=attr(full.get("title", slug)),
            title_en_attr=attr(english.get("title", full.get("title", slug))),
            summary_attr=attr(full.get("summary", "")),
            summary_en_attr=attr(english.get("summary", full.get("summary", ""))),
            tags_attr=attr(" ".join("#" + x for x in full.get("tags", []))),
            tags_en_attr=attr(" ".join("#" + x for x in english.get("tags", full.get("tags", []))),
            ),
        )
        (article_dir / "index.html").write_text(
            shell(
                full.get("title", slug), body, "../../",
                english.get("title", full.get("title", slug)),
            ), encoding="utf-8",
        )
        cards.append("""<li><a href="post/{slug}/"><time>{date}</time>
<h2 data-zh="{title_attr}" data-en="{title_en_attr}">{title}</h2>
<p data-zh="{summary_attr}" data-en="{summary_en_attr}">{summary}</p>
<span data-zh="{tags_attr}" data-en="{tags_en_attr}">{tags}</span></a></li>""".format(
            slug=slug, date=html.escape(str(full.get("date", ""))),
            title=html.escape(full.get("title", slug)),
            summary=html.escape(full.get("summary", "")), tags=tags,
            title_attr=attr(full.get("title", slug)),
            title_en_attr=attr(english.get("title", full.get("title", slug))),
            summary_attr=attr(full.get("summary", "")),
            summary_en_attr=attr(english.get("summary", full.get("summary", ""))),
            tags_attr=attr(" ".join("#" + x for x in full.get("tags", []))),
            tags_en_attr=attr(" ".join("#" + x for x in english.get("tags", full.get("tags", []))),
            ),
        ))
        manifest.append({key: full.get(key) for key in (
            "slug", "title", "date", "summary", "tags", "reading_time"
        )})
    body = """<section class="intro"><h1 data-zh="智能座舱与汽车软件" data-en="Smart Cockpit & Automotive Software">智能座舱与汽车软件</h1>
<p data-zh="服务器博客的 GitHub Pages 静态镜像，文章原文同时保存在仓库中。" data-en="A static GitHub Pages mirror of the server blog. The Markdown sources are preserved in this repository.">服务器博客的 GitHub Pages 静态镜像，文章原文同时保存在仓库中。</p></section>
<ul class="posts">{}</ul>""".format("".join(cards))
    (OUT / "index.html").write_text(shell("技术文章", body, en_title="Technical Articles"), encoding="utf-8")
    (OUT / "articles.json").write_text(
        json.dumps({"source": ORIGIN, "items": manifest}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    translation_path.write_text(
        json.dumps(translations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUT / "static" / "crane-hero.jpg").write_bytes(fetch_bytes("/static/crane-hero.jpg"))
    print("synced {} articles".format(len(items)))


if __name__ == "__main__":
    main()
