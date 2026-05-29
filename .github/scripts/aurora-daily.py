#!/usr/bin/env python3
"""Daily aurora forecast & Norway travel news updater."""
import json, urllib.request, re, os, sys
from datetime import date

HTML_FILE = "travel_plan_v2.html"
MARKER_START = "<!-- DAILY_UPDATES_START -->"
MARKER_END   = "<!-- DAILY_UPDATES_END -->"

today = date.today().isoformat()

# --- Fetch Kp index ---
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

# --- Fetch 3-day forecast ---
forecast_html = ""
try:
    with urllib.request.urlopen("https://services.swpc.noaa.gov/products/aurora/3day_forecast.json", timeout=10) as r:
        fc = json.loads(r.read())
        for row in fc[1:4]:
            d = row[0][:10]
            kp_high = row[2]
            forecast_html += f'<span style="font-size:0.68rem;background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.15);border-radius:6px;padding:3px 8px;color:var(--aurora-green);">{d} · Kp {kp_high}</span> '
except Exception as e:
    print(f"Forecast fetch failed: {e}")

# --- Fetch news ---
news_html = ""
try:
    with urllib.request.urlopen("https://news.google.com/rss/search?q=norway+aurora+travel+2026&hl=en-US&gl=US&ceid=US:en", timeout=10) as r:
        xml = r.read().decode()
        titles = re.findall(r'<title>(.*?)</title>', xml)
        for t in titles[1:6]:  # skip first which is feed title
            t = t.replace("&#39;", "'").strip()
            if t and "Google News" not in t:
                news_html += f'<div style="font-size:0.68rem;padding:3px 0;color:var(--text-secondary);border-bottom:1px solid rgba(148,163,184,0.1);">📰 {t}</div>'
except Exception as e:
    print(f"News fetch failed: {e}")

if not news_html:
    news_html = '<div style="font-size:0.68rem;color:var(--text-secondary);">📡 今日暂无新资讯</div>'

# --- Build card ---
card = f"""<!-- DAILY_UPDATES_START -->
<div class="section-header" style="border-left:3px solid var(--aurora-green);background:linear-gradient(135deg,rgba(57,255,20,0.06),rgba(180,77,255,0.06));">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">
    <span style="font-weight:600;color:var(--aurora-green);font-size:0.8rem;">📡 每日极光快报 · {today}</span>
    <span style="font-size:0.6rem;color:var(--text-secondary);background:rgba(57,255,20,0.08);padding:2px 8px;border-radius:10px;border:1px solid rgba(57,255,20,0.15);">实时 Kp: {kp_data["kp"]} <span style="color:{kp_data["color"]};">●</span> {kp_data["label"]}</span>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;">
    {forecast_html}
  </div>
  <div style="margin-top:8px;">
    {news_html}
  </div>
  <div style="margin-top:6px;font-size:0.55rem;color:var(--text-secondary);opacity:0.5;text-align:right;">数据来源: NOAA · Google News · 自动更新</div>
</div>
<!-- DAILY_UPDATES_END -->"""

# --- Update HTML ---
if not os.path.exists(HTML_FILE):
    print(f"{HTML_FILE} not found!"); sys.exit(1)

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

if MARKER_START in html:
    # Replace existing update block
    pattern = re.compile(re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(card, html)
        print("Updated existing daily update block.")
    else:
        print("Markers found but pattern didn't match.")
else:
    # Insert after hero section
    insert_after = '<div class="hero-timeline'
    idx = html.find(insert_after)
    if idx == -1:
        # fallback: after first section-header
        idx = html.find('<div class="section-header"')
    if idx > 0:
        # Find end of this div
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
print("✅ Daily update complete.")
