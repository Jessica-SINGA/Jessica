#!/usr/bin/env python3
"""Daily Norway travel news aggregator + aurora forecast + exchange rate."""
import json, urllib.request, re, os, sys
from datetime import date, datetime

HTML_FILE = "travel_plan_v2.html"
MARKER_START = "<!-- DAILY_UPDATES_START -->"
MARKER_END   = "<!-- DAILY_UPDATES_END -->"

today = date.today().isoformat()

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
    print(f"Kp fetch failed: {e}")

# ===== Fetch 3-day forecast =====
forecast_html = ""
try:
    with urllib.request.urlopen("https://services.swpc.noaa.gov/products/aurora/3day_forecast.json", timeout=10) as r:
        fc = json.loads(r.read())
        for row in fc[1:4]:
            d = row[0][:10]
            kp_high = row[2]
            forecast_html += f'<span style="font-size:0.65rem;background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.15);border-radius:6px;padding:2px 8px;color:var(--aurora-green);">{d} Kp {kp_high}</span> '
except Exception as e:
    print(f"Forecast fetch failed: {e}")

# ===== Fetch exchange rate (NOK → CNY) =====
rate_html = ""
try:
    with urllib.request.urlopen("https://api.exchangerate-api.com/v4/latest/NOK", timeout=10) as r:
        data = json.loads(r.read())
        cny = data["rates"].get("CNY", "N/A")
        usd = data["rates"].get("USD", "N/A")
        rate_html = f'💱 1 NOK = {cny} CNY · 1 NOK = {usd} USD'
        print(f"Exchange rate: {rate_html}")
except Exception as e:
    rate_html = "💱 汇率数据暂不可用"
    print(f"Exchange rate fetch failed: {e}")

# ===== Fetch news from multiple sources =====
all_news = []
seen_titles = set()

def fetch_rss(url, source_label, max_items=5):
    """Fetch RSS and extract news items."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read().decode("utf-8", errors="ignore")
            titles = re.findall(r'<title>(.*?)</title>', xml)
            links = re.findall(r'<link>(.*?)</link>', xml)
            added = 0
            for i, t in enumerate(titles):
                t = t.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").strip()
                if not t or len(t) < 8 or "Google News" in t:
                    continue
                if t not in seen_titles:
                    seen_titles.add(t)
                    link = links[i] if i < len(links) and links[i].startswith("http") else ""
                    all_news.append((t, source_label, link))
                    added += 1
                    if added >= max_items:
                        break
    except Exception as e:
        print(f"RSS {source_label} failed: {e}")

# English sources
fetch_rss("https://news.google.com/rss/search?q=norway+travel+aurora+2026&hl=en-US&gl=US&ceid=US:en", "Google News EN")
fetch_rss("https://www.visitnorway.com/rss/news", "Visit Norway")
fetch_rss("https://www.thelocal.no/feed/rss", "The Local Norway")

# Chinese sources
fetch_rss("https://news.google.com/rss/search?q=挪威+旅游+极光+2026&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")
fetch_rss("https://news.google.com/rss/search?q=挪威+旅行+攻略&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")

# Group by source
news_by_source = {}
for title, source, link in all_news:
    if source not in news_by_source:
        news_by_source[source] = []
    news_by_source[source].append((title, link))

# Build news HTML
news_html = ""
source_icons = {
    "Google News EN": "📰",
    "Google News CN": "📰",
    "Visit Norway": "🇳🇴",
    "The Local Norway": "📋",
}
if news_by_source:
    for src, items in news_by_source.items():
        icon = source_icons.get(src, "📌")
        news_html += f'<div style="font-size:0.65rem;font-weight:600;color:var(--text-secondary);margin-top:6px;">{icon} {src}</div>'
        for title, link in items[:4]:
            title_short = title if len(title) < 90 else title[:87] + "..."
            news_html += f'<div style="font-size:0.68rem;padding:3px 0 3px 10px;color:var(--text-secondary);border-bottom:1px solid rgba(148,163,184,0.08);border-left:2px solid rgba(57,255,20,0.2);margin-bottom:2px;">{title_short}</div>'
else:
    news_html = '<div style="font-size:0.68rem;color:var(--text-secondary);">📡 今日暂无新资讯</div>'

# ===== Build card =====
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
  <div style="margin-top:6px;font-size:0.5rem;color:var(--text-secondary);opacity:0.4;text-align:right;">来源: NOAA · Google News · Visit Norway · 每日自动更新</div>
</div>
<!-- DAILY_UPDATES_END -->"""

# ===== Update HTML =====
if not os.path.exists(HTML_FILE):
    print(f"{HTML_FILE} not found!"); sys.exit(1)

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

if MARKER_START in html:
    pattern = re.compile(re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(card, html)
        print("Updated existing daily update block.")
    else:
        print("Markers found but pattern didn't match.")
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
                print(f"Inserted daily update card at position {insert_pos}.")
            else: print("Could not find div closure."); sys.exit(1)
        else: print("Could not find div closure."); sys.exit(1)
    else: print("Could not find insertion point."); sys.exit(1)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print("✅ Daily Norway update complete.")
