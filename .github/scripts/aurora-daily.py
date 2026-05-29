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
    pass

def translate(text, max_len=2000):
    if not text or len(text) < 5 or translator is None:
        return text
    try:
        return translator.translate(text[:max_len], dest='zh-cn').text
    except:
        try:
            return translator.translate(text[:1000], dest='zh-cn').text
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
        rate_html = f'1 NOK = {cny} CNY / 1 NOK = {usd} USD'
        rate_plain = f"1 NOK = {cny} CNY / 1 NOK = {usd} USD"
        safe_print(f"Exchange rate: {rate_html}")
except Exception as e:
    rate_html = "Hui rate N/A"
    rate_plain = "Hui rate N/A"
    safe_print(f"Exchange rate fetch failed: {e}")

# ===== Fetch news from multiple sources =====
all_news = []  # (title, source, desc)
seen_titles = set()

def clean_html(raw):
    text = re.sub(r'<[^>]+>', ' ', raw)  # replace tags with space
    text = html_mod.unescape(text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\b\w+\.(jpg|png|gif|svg|webp)\b', '', text, flags=re.I)
    text = re.sub(r'\s+', ' ', text).strip()
    # Validate: skip if too short or looks like nav text
    if len(text) < 20 or text in ('', 'Google News', 'Home'):
        return ""
    # Remove trailing date/source fragments like " - 2026-05-30"
    text = re.sub(r'\s*[–—-]\s*\d{4}.*$', '', text)
    return text[:350]

def fetch_rss(url, source_label, max_items=3):
    try:
        # Encode URL for non-ASCII characters
        url_encoded = urllib.parse.quote(url, safe='/:?=&')
        req = urllib.request.Request(url_encoded, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read().decode("utf-8", errors="ignore")
            items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
            if not items:
                items = re.findall(r'<entry>(.*?)</entry>', xml, re.DOTALL)

            added = 0
            for item_xml in items:
                t_match = re.search(r'<title>(.*?)</title>', item_xml, re.DOTALL)
                if not t_match:
                    continue
                t = t_match.group(1)
                t = t.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").strip()
                if not t or len(t) < 8 or "Google News" in t:
                    continue
                if t in seen_titles:
                    continue

                # Extract and clean description
                desc = ""
                d_match = re.search(r'<description>(.*?)</description>', item_xml, re.DOTALL)
                if d_match:
                    d_raw = d_match.group(1)
                    # Strip CDATA wrapper if present
                    d_raw = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', d_raw, flags=re.DOTALL)
                    desc = clean_html(d_raw)

                seen_titles.add(t)

                # Translate to Chinese
                if source_label in ("Google News", "Lonely Planet", "The Local Norway"):
                    try:
                        t_cn = translate(t)
                        if t_cn and t_cn != t:
                            t = t_cn
                    except:
                        pass
                    if desc:
                        try:
                            desc_cn = translate(desc)
                            if desc_cn and desc_cn != desc:
                                desc = desc_cn
                        except:
                            pass

                all_news.append((t, source_label, desc))
                added += 1
                if added >= max_items:
                    break
    except Exception as e:
        safe_print(f"RSS {source_label} failed: {e}")

# English sources (will be translated)
fetch_rss("https://news.google.com/rss/search?q=norway+travel+aurora+2026&hl=en-US&gl=US&ceid=US:en", "Google News")
fetch_rss("https://www.lonelyplanet.com/rss/articles", "Lonely Planet")

# Chinese social & travel platform content via Google News search
fetch_rss("https://news.google.com/rss/search?q=site:xiaohongshu.com+挪威+旅游+攻略+2026&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "小红书攻略")
fetch_rss("https://news.google.com/rss/search?q=site:mafengwo.cn+挪威+极光+攻略&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "马蜂窝攻略")
fetch_rss("https://news.google.com/rss/search?q=挪威+旅游+最新攻略+费用+路线+2026&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")
fetch_rss("https://news.google.com/rss/search?q=挪威+极光+自由行+住宿+交通+签证&hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "Google News CN")

# Bing News as backup Chinese source
fetch_rss("https://www.bing.com/news/search?q=挪威+旅游+极光+2026&format=rss", "Bing News")

# Build display
news_by_source = {}
for title, source, desc in all_news:
    if source not in news_by_source:
        news_by_source[source] = []
    news_by_source[source].append((title, desc))

news_html = ""
if news_by_source:
    for src, items in news_by_source.items():
        news_html += f'<div style="font-size:0.62rem;font-weight:600;color:var(--text-secondary);margin-top:8px;">{src}</div>'
        for title, desc in items[:3]:
            t_short = title if len(title) < 80 else title[:77] + "..."
            news_html += f'<div style="font-size:0.67rem;padding:4px 0 1px 10px;color:var(--text-primary);border-left:2px solid rgba(57,255,20,0.25);">+ {t_short}</div>'
            if desc:
                d_short = desc if len(desc) < 150 else desc[:147] + "..."
                news_html += f'<div style="font-size:0.6rem;padding:0 0 5px 10px;color:var(--text-muted);border-left:2px solid rgba(57,255,20,0.25);border-bottom:1px solid rgba(148,163,184,0.06);margin-bottom:4px;line-height:1.5;">  {d_short}</div>'
            else:
                news_html += f'<div style="font-size:0.55rem;padding:0 0 5px 10px;color:var(--text-muted);border-left:2px solid rgba(57,255,20,0.25);border-bottom:1px solid rgba(148,163,184,0.06);margin-bottom:4px;">  暂无详细内容</div>'
else:
    news_html = '<div style="font-size:0.68rem;color:var(--text-secondary);">今日暂无新资讯</div>'

# Build archive data
news_archive = {}
for src, items in news_by_source.items():
    news_archive[src] = [{"title": t, "desc": d} for t, d in items[:5]]

archive_entry = {
    "date": today,
    "kp": kp_data["kp"],
    "kp_label": kp_data["label"],
    "kp_color": kp_data["color"],
    "forecast": forecast_list,
    "exchange_rate": rate_plain,
    "news": news_archive,
}

# Write to archive JSON
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

# Build card for main page
card = f"""<!-- DAILY_UPDATES_START -->
<div class="section-header" style="border-left:3px solid var(--aurora-green);background:linear-gradient(135deg,rgba(57,255,20,0.06),rgba(180,77,255,0.06));">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">
    <span style="font-weight:600;color:var(--aurora-green);font-size:0.75rem;">Norway Daily News {today}</span>
    <span style="font-size:0.55rem;color:var(--text-secondary);background:rgba(57,255,20,0.08);padding:2px 8px;border-radius:10px;border:1px solid rgba(57,255,20,0.15);">Kp: {kp_data["kp"]} <span style="color:{kp_data["color"]};">●</span> {kp_data["label"]}</span>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;align-items:center;">
    <span style="font-size:0.65rem;color:var(--aurora-green);">3-day forecast:</span>
    {forecast_html}
  </div>
  <div style="margin-top:6px;font-size:0.65rem;color:var(--gold, #ffd700);padding:4px 8px;background:rgba(255,215,0,0.06);border-radius:6px;border:1px solid rgba(255,215,0,0.12);">
    {rate_html}
  </div>
  <div style="margin-top:10px;border-top:1px solid rgba(148,163,184,0.15);padding-top:8px;">
    <div style="font-size:0.7rem;font-weight:600;color:var(--text-primary);margin-bottom:4px;">Norway Travel News Summary</div>
    {news_html}
  </div>
  <div style="margin-top:8px;display:flex;justify-content:space-between;align-items:center;font-size:0.55rem;color:var(--text-secondary);">
    <span style="opacity:0.4;">NOAA Google News Lonely Planet auto update</span>
    <a href="norway-news-archive.html" style="color:var(--aurora-green);text-decoration:none;border:1px solid rgba(57,255,20,0.2);border-radius:12px;padding:3px 10px;font-size:0.6rem;">View history -></a>
  </div>
</div>
<!-- DAILY_UPDATES_END -->"""

# Update HTML
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
