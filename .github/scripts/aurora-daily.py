#!/usr/bin/env python3
"""Daily Norway travel news aggregator + aurora forecast + exchange rate + archive."""
import json, urllib.request, urllib.parse, re, os, sys, html as html_mod
from datetime import date, datetime

HTML_FILE = "travel_plan_v2.html"
ARCHIVE_FILE = "norway-news-data.json"
MARKER_START = "<!-- DAILY_UPDATES_START -->"
MARKER_END   = "<!-- DAILY_UPDATES_END -->"

today = date.today().isoformat()

# ----- Translation -----
translator = None
try:
    from googletrans import Translator
    translator = Translator()
except:
    try:
        from translate import Translator as T2
        translator = T2(to_lang="zh")
    except:
        pass

def translate(text):
    if not text or len(text) < 5:
        return text
    if translator is None:
        return text
    try:
        if hasattr(translator, 'translate') and not hasattr(translator, 'to_lang'):
            return translator.translate(text[:2000], dest='zh-cn').text
        elif hasattr(translator, 'translate'):
            return translator.translate(text[:2000])
        return text
    except:
        return text

def safe_print(msg):
    try:
        print(msg)
    except:
        print(str(msg.encode("utf-8", errors="replace")))

# ===== Fetch Kp index =====
kp_data = {"kp": "N/A", "label": "平静", "color": "#94a3b8"}
try:
    with urllib.request.urlopen("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json", timeout=10) as r:
        rows = json.loads(r.read())
        if rows:
            kp = float(rows[-1]["kp_index"])
            kp_data["kp"] = str(kp)
            if kp >= 7:    kp_data["label"] = "强风暴 ⚠️"; kp_data["color"] = "#ef4444"
            elif kp >= 5:  kp_data["label"] = "活跃 🌤️";   kp_data["color"] = "#fb923c"
            elif kp >= 3:  kp_data["label"] = "中等 ✅";    kp_data["color"] = "#39ff14"
            else:          kp_data["label"] = "平静";       kp_data["color"] = "#94a3b8"
except Exception as e:
    safe_print(f"Kp fetch failed: {e}")

# ===== Fetch 3-day forecast =====
forecast_html = ""
forecast_list = []
try:
    with urllib.request.urlopen("https://services.swpc.noaa.gov/products/aurora/3day_forecast.json", timeout=10) as r:
        fc = json.loads(r.read())
        for row in fc[1:4]:
            d = row[0][:10]
            kp_high = row[2]
            forecast_html += f'<span style="font-size:0.65rem;background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.15);border-radius:6px;padding:2px 8px;color:var(--aurora-green);">{d} Kp {kp_high}</span> '
            forecast_list.append(f"{d} Kp {kp_high}")
except Exception as e:
    safe_print(f"Forecast fetch failed: {e}")

# ===== Fetch exchange rate (NOK -> CNY) =====
rate_html = ""
rate_plain = ""
try:
    with urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/NOK", timeout=10) as r:
        data = json.loads(r.read())
        cny = data["rates"].get("CNY", "N/A")
        usd = data["rates"].get("USD", "N/A")
        rate_html = f'💱 1 NOK = {cny} CNY · 1 NOK = {usd} USD'
        rate_plain = f"1 NOK = {cny} CNY · 1 NOK = {usd} USD"
        safe_print(f"Exchange rate: {rate_html}")
except Exception as e:
    rate_html = "💱 汇率数据暂不可用"
    rate_plain = "汇率数据暂不可用"
    safe_print(f"Exchange rate fetch failed: {e}")

# ===== Fetch news from multiple sources =====
all_news = []  # (title, source, link, description)
seen_titles = set()

def clean_html(raw):
    """Strip HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', raw)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_rss(url, source_label, max_items=4):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read().decode("utf-8", errors="ignore")

            titles = re.findall(r'<title>(.*?)</title>', xml, re.DOTALL)
            links = re.findall(r'<link>(.*?)</link>', xml, re.DOTALL)
            descs = re.findall(r'<description>(.*?)</description>', xml, re.DOTALL)

            # Handle CDATA in descriptions
            descs = [re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', d) for d in descs]

            # Google News RSS has description after each item, offset by 1
            # (first <description> is channel-level)
            if source_label.startswith("Google News"):
                if len(descs) > 1:
                    descs = descs[1:]  # skip channel description

            added = 0
            for i, t in enumerate(titles):
                t = t.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").strip()
                if not t or len(t) < 8 or "Google News" in t:
                    continue
                if t not in seen_titles:
                    seen_titles.add(t)
                    link = links[i] if i < len(links) and links[i].startswith("http") else ""

                    desc = ""
                    if i < len(descs):
                        desc = clean_html(descs[i])
                    if not desc or len(desc) < 10:
                        desc = ""

                    all_news.append((t, source_label, link, desc))
                    added += 1
                    if added >= max_items:
                        break
    except Exception as e:
        safe_print(f"RSS {source_label} failed: {e}")

# English sources
fetch_rss("https://news.google.com/rss/search?q=norway+travel+aurora+2026&hl=en-US&gl=US&ceid=US:en", "Google News")
fetch_rss("https://www.lonelyplanet.com/rss/articles", "Lonely Planet")
fetch_rss("https://www.thelocal.no/feed/rss", "The Local Norway")

# Chinese sources - search with Chinese keywords
fetch_rss("https://news.google.com/rss/search?q=挪威+旅游+极光+攻略+2026&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")
fetch_rss("https://news.google.com/rss/search?q=挪威+旅行+签证+机票+攻略&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")
fetch_rss("https://news.google.com/rss/search?q=挪威+极光+自由行+费用&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")

# Group by source, translate content
news_by_source = {}
for title, source, link, desc in all_news:
    if source not in news_by_source:
        news_by_source[source] = []
    news_by_source[source].append((title, link, desc))

news_html = ""
source_icons = {
    "Google News": "📰",
    "Google News CN": "📰",
    "Lonely Planet": "🌍",
    "The Local Norway": "📋",
}
if news_by_source:
    for src, items in news_by_source.items():
        icon = source_icons.get(src, "📌")
        news_html += f'<div style="font-size:0.65rem;font-weight:600;color:var(--text-secondary);margin-top:6px;">{icon} {src}</div>'
        for title, link, desc in items[:3]:
            title_short = title if len(title) < 80 else title[:77] + "..."
            news_html += f'<div style="font-size:0.68rem;padding:4px 0 2px 10px;color:var(--text-primary);border-left:2px solid rgba(57,255,20,0.25);margin-bottom:1px;">{title_short}</div>'
            if desc:
                desc_short = desc if len(desc) < 120 else desc[:117] + "..."
                news_html += f'<div style="font-size:0.6rem;padding:0 0 4px 10px;color:var(--text-muted);border-left:2px solid rgba(57,255,20,0.25);border-bottom:1px solid rgba(148,163,184,0.06);margin-bottom:4px;">{desc_short}</div>'
            else:
                news_html += f'<div style="font-size:0.58rem;padding:0 0 4px 10px;color:var(--text-muted);border-left:2px solid rgba(57,255,20,0.25);border-bottom:1px solid rgba(148,163,184,0.06);margin-bottom:4px;">暂无摘要</div>'
else:
    news_html = '<div style="font-size:0.68rem;color:var(--text-secondary);">📡 今日暂无新资讯</div>'

# Build plain data for JSON archive (with translation)
news_archive = {}
for src, items in news_by_source.items():
    news_archive[src] = []
    for title, link, desc in items[:5]:
        entry = {"title": title}
        if desc:
            # Try translating description
            entry["desc"] = desc
        news_archive[src].append(entry)

archive_entry = {
    "date": today,
    "kp": kp_data["kp"],
    "kp_label": kp_data["label"],
    "kp_color": kp_data["color"],
    "forecast": forecast_list,
    "exchange_rate": rate_plain,
    "news": news_archive,
}

# ===== Write to archive JSON =====
archive_data = []
if os.path.exists(ARCHIVE_FILE):
    try:
        with open(ARCHIVE_FILE, encoding="utf-8") as f:
            existing = json.load(f)
        if isinstance(existing, list):
            archive_data = existing
    except Exception as e:
        safe_print(f"Read archive failed: {e}")

archive_data.insert(0, archive_entry)
archive_data = archive_data[:90]

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive_data, f, ensure_ascii=False, indent=2)
safe_print(f"Archive updated: {len(archive_data)} days")

# ===== Build card for main page =====
card = f"""<!-- DAILY_UPDATES_START -->
<div class="section-header" style="border-left:3px solid var(--aurora-green);background:linear-gradient(135deg,rgba(57,255,20,0.06),rgba(180,77,255,0.06));">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">
    <span style="font-weight:600;color:var(--aurora-green);font-size:0.75rem;">📡 每日挪威资讯 · {today}</span>
    <span style="font-size:0.55rem;color:var(--text-secondary);background:rgba(57,255,20,0.08);padding:2px 8px;border-radius:10px;border:1px solid rgba(57,255,20,0.15);">实时 Kp: {kp_data["kp"]} <span style="color:{kp_data["color"]};">●</span> {kp_data["label"]}</span>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;align-items:center;">
    <span style="font-size:0.65rem;color:var(--aurora-green);">🌌 未来3天预报:</span>
    {forecast_html}
  </div>
  <div style="margin-top:6px;font-size:0.65rem;color:var(--gold, #ffd700);padding:4px 8px;background:rgba(255,215,0,0.06);border-radius:6px;border:1px solid rgba(255,215,0,0.12);">
    {rate_html}
  </div>
  <div style="margin-top:10px;border-top:1px solid rgba(148,163,184,0.15);padding-top:8px;">
    <div style="font-size:0.7rem;font-weight:600;color:var(--text-primary);margin-bottom:4px;">📋 最新挪威旅行资讯</div>
    {news_html}
  </div>
  <div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center;font-size:0.55rem;color:var(--text-secondary);">
    <span style="opacity:0.4;">来源: NOAA · Google News · Lonely Planet · 每日自动更新</span>
    <a href="norway-news-archive.html" style="color:var(--aurora-green);text-decoration:none;border:1px solid rgba(57,255,20,0.2);border-radius:12px;padding:3px 10px;font-size:0.6rem;">查看历史资讯 →</a>
  </div>
</div>
<!-- DAILY_UPDATES_END -->"""

# ===== Update HTML =====
if not os.path.exists(HTML_FILE):
    safe_print(f"{HTML_FILE} not found!"); sys.exit(1)

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

if MARKER_START in html:
    pattern = re.compile(re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(card, html)
        safe_print("Updated existing daily update block.")
    else:
        safe_print("Markers found but pattern didn't match.")
else:
    insert_after = '<div class="hero-timeline'
    idx = html.find(insert_after)
    if idx == -1:
        idx = html.find('<div class="section-header"')
    if idx > 0:
        close_idx = html.find("</div>", idx)
        if close_idx > 0:
            close_idx = html.find("</div>", close_idx + 6)
            if close_idx > 0:
                close_idx = html.find("</div>", close_idx + 6)
                insert_pos = close_idx + 6
                html = html[:insert_pos] + "\n\n" + card + "\n" + html[insert_pos:]
                safe_print(f"Inserted daily update card at position {insert_pos}.")
            else: safe_print("Could not find div closure."); sys.exit(1)
        else: safe_print("Could not find div closure."); sys.exit(1)
    else: safe_print("Could not find insertion point."); sys.exit(1)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)
safe_print("Daily Norway update complete.")
