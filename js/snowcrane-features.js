(function () {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("snowcrane-theme") || "dark";
  const savedLang = localStorage.getItem("snowcrane-lang") || "zh";
  root.dataset.theme = savedTheme;

  const labels = {
    zh: { search: "搜索", archive: "归档", theme: "主题", lang: "EN", placeholder: "搜索标题、摘要和正文", empty: "没有找到相关文章", unavailable: "这篇历史文章暂时只有中文正文", archiveTab: "时间轴", tagTab: "标签", categoryTab: "分类", total: "共" },
    en: { search: "Search", archive: "Archive", theme: "Theme", lang: "中文", placeholder: "Search titles, summaries and content", empty: "No matching articles", unavailable: "This archived article is currently available in Chinese only", archiveTab: "Archive", tagTab: "Tag", categoryTab: "Category", total: "Total" }
  };
  let lang = savedLang === "en" ? "en" : "zh";

  const toolbar = document.createElement("div");
  toolbar.className = "sc-toolbar";
  toolbar.innerHTML = '<button data-action="search">⌕</button><button data-action="archive">▤</button><button data-action="theme">◐</button><button data-action="lang"></button><a href="/" data-action="home">⌂</a>';
  document.body.appendChild(toolbar);

  const modal = document.createElement("div");
  modal.className = "sc-search";
  modal.hidden = true;
  modal.innerHTML = '<div class="sc-search-card"><button class="sc-close" aria-label="Close">×</button><input type="search"><div class="sc-results"></div></div>';
  document.body.appendChild(modal);
  const drawer = document.createElement("aside");
  drawer.className = "sc-archive";
  drawer.hidden = true;
  drawer.innerHTML = '<div class="sc-archive-head"><div class="sc-tabs"><button data-tab="archive"></button><button data-tab="tag"></button><button data-tab="category"></button></div><button class="sc-archive-close">×</button></div><div class="sc-archive-body"></div>';
  document.body.appendChild(drawer);
  const archiveTab = document.createElement("button");
  archiveTab.className = "sc-archive-tab";
  archiveTab.type = "button";
  document.body.appendChild(archiveTab);
  const input = modal.querySelector("input");
  const results = modal.querySelector(".sc-results");
  let index;
  let archiveIndex;

  function updateLabels() {
    const t = labels[lang];
    toolbar.querySelector('[data-action="search"]').title = t.search;
    toolbar.querySelector('[data-action="archive"]').title = t.archive;
    toolbar.querySelector('[data-action="theme"]').title = t.theme;
    toolbar.querySelector('[data-action="lang"]').textContent = t.lang;
    toolbar.querySelector('[data-action="home"]').title = lang === "en" ? "Home" : "首页";
    drawer.querySelector('[data-tab="archive"]').textContent = "▱ " + t.archiveTab;
    drawer.querySelector('[data-tab="tag"]').textContent = "◇ " + t.tagTab;
    drawer.querySelector('[data-tab="category"]').textContent = "□ " + t.categoryTab;
    archiveTab.textContent = "◷ " + t.archiveTab;
    input.placeholder = t.placeholder;
  }
  function showMessage(message) {
    let toast = document.querySelector(".sc-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "sc-toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2600);
  }
  async function openSearch() {
    modal.hidden = false;
    input.focus();
    if (!index) index = await fetch("/search-index.json").then(r => r.json());
    renderResults("");
  }
  async function openArchive() {
    if (!drawer.hidden) {
      drawer.hidden = true;
      archiveTab.classList.remove("open");
      return;
    }
    drawer.hidden = false;
    archiveTab.classList.add("open");
    if (!archiveIndex) archiveIndex = await fetch("/archive-index.json").then(r => r.json());
    renderArchive("archive");
  }
  function renderArchive(tab, filter) {
    const items = archiveIndex.items;
    drawer.querySelectorAll("[data-tab]").forEach(button => button.classList.toggle("active", button.dataset.tab === tab));
    const body = drawer.querySelector(".sc-archive-body");
    if (tab === "archive") {
      const years = {};
      items.forEach(item => (years[item.date.slice(0, 4) || "Earlier"] ||= []).push(item));
      body.innerHTML = '<p class="sc-total">' + labels[lang].total + ' · ' + items.length + '</p>' +
        Object.keys(years).sort().reverse().map(year =>
          '<section><h3>' + year + '</h3><ul>' + years[year].map(item =>
            '<li><time>' + item.date.slice(5) + '</time><a href="' + item.path + '">' + escapeHtml(item.title) + '</a></li>'
          ).join("") + '</ul></section>'
        ).join("");
      return;
    }
    const key = tab === "tag" ? "tags" : "categories";
    const groups = {};
    items.forEach(item => (item[key] || []).forEach(name => (groups[name] ||= []).push(item)));
    if (!filter) {
      body.innerHTML = '<div class="sc-cloud">' + Object.keys(groups).sort().map(name =>
        '<button data-filter="' + escapeHtml(name) + '">' + escapeHtml(name) + ' <small>' + groups[name].length + '</small></button>'
      ).join("") + '</div>';
      body.querySelectorAll("[data-filter]").forEach(button => button.onclick = () => renderArchive(tab, button.dataset.filter));
    } else {
      body.innerHTML = '<button class="sc-filter-back">← ' + escapeHtml(filter) + '</button><ul class="sc-filter-list">' +
        groups[filter].map(item => '<li><time>' + item.date + '</time><a href="' + item.path + '">' + escapeHtml(item.title) + '</a></li>').join("") + '</ul>';
      body.querySelector(".sc-filter-back").onclick = () => renderArchive(tab);
    }
  }
  function renderResults(query) {
    if (!index) return;
    const words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    const found = index.items.filter(item => {
      const haystack = (item.title + " " + item.summary + " " + item.text).toLowerCase();
      return words.every(word => haystack.includes(word));
    }).slice(0, 30);
    results.innerHTML = found.map(item =>
      '<a href="' + item.path + '"><time>' + item.date + '</time><strong>' +
      escapeHtml(item.title) + '</strong><span>' + escapeHtml(item.summary || "") + '</span></a>'
    ).join("") || '<p>' + labels[lang].empty + '</p>';
  }
  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  toolbar.querySelector('[data-action="search"]').onclick = openSearch;
  toolbar.querySelector('[data-action="archive"]').onclick = openArchive;
  archiveTab.onclick = openArchive;
  toolbar.querySelector('[data-action="theme"]').onclick = function () {
    root.dataset.theme = root.dataset.theme === "light" ? "dark" : "light";
    localStorage.setItem("snowcrane-theme", root.dataset.theme);
  };
  toolbar.querySelector('[data-action="lang"]').onclick = function () {
    lang = lang === "zh" ? "en" : "zh";
    localStorage.setItem("snowcrane-lang", lang);
    const articleToggle = document.getElementById("langToggle");
    if (articleToggle) articleToggle.click();
    else if (lang === "en" && location.pathname.startsWith("/article/")) showMessage(labels.en.unavailable);
    root.lang = lang === "en" ? "en" : "zh-CN";
    updateLabels();
  };
  modal.querySelector(".sc-close").onclick = () => { modal.hidden = true; };
  drawer.querySelector(".sc-archive-close").onclick = () => { drawer.hidden = true; archiveTab.classList.remove("open"); };
  drawer.querySelectorAll("[data-tab]").forEach(button => button.onclick = () => renderArchive(button.dataset.tab));
  modal.onclick = e => { if (e.target === modal) modal.hidden = true; };
  input.oninput = () => renderResults(input.value);
  document.addEventListener("keydown", e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openSearch(); }
    if (e.key === "Escape") { modal.hidden = true; drawer.hidden = true; archiveTab.classList.remove("open"); }
  });
  updateLabels();
})();
