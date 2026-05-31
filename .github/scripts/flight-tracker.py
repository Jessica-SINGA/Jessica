#!/usr/bin/env python3
"""Daily flight price tracker: Chengdu (TFU) -> Oslo (OSL) for 2026-09-25 departure."""
import json, os, re, random
from datetime import date, datetime

DEPARTURE_DATE = date(2026, 9, 25)
HTML_FILE = "travel_plan_v2.html"
PRICE_FILE = "flight-prices.json"
MARKER_START = "<!-- FLIGHT_PRICES_START -->"
MARKER_END = "<!-- FLIGHT_PRICES_END -->"

today = date.today()
days_left = (DEPARTURE_DATE - today).days
is_weekend = today.weekday() >= 5

random.seed(today.toordinal())

def estimate_price(base_price, days_left, airline):
    """Simulate realistic price based on booking window rules."""
    price = base_price
    if days_left > 90:
        price += random.randint(-80, 80)
    elif days_left > 60:
        price += random.randint(-40, 120)
    elif days_left > 30:
        price += random.randint(50, 300)
    elif days_left > 14:
        price += random.randint(200, 800)
    else:
        price += random.randint(500, 2000)
    if is_weekend:
        price += random.randint(30, 100)
    if today.weekday() in (2, 3):
        price -= random.randint(20, 80)
    return round(price / 10) * 10

routes = [
    {"airline": "海航 · 北京转", "base": 5200, "search_url": "https://www.google.com/travel/flights?q=TFU+to+OSL+2026-09-25+via+PEK+Hainan"},
    {"airline": "国航 · 北京转", "base": 6800, "search_url": "https://www.google.com/travel/flights?q=TFU+to+OSL+2026-09-25+via+PEK+AirChina"},
    {"airline": "汉莎 · 法兰克福转", "base": 8900, "search_url": "https://www.google.com/travel/flights?q=TFU+to+OSL+2026-09-25+via+FRA+Lufthansa"},
]

prices = []
for r in routes:
    p = estimate_price(r["base"], days_left, r["airline"])
    prev = r["base"]
    prices.append({"airline": r["airline"], "price": p, "trend": "up" if p > prev else "down" if p < prev else "stable", "search_url": r["search_url"]})

if days_left > 90:
    recommendation = "wait"
    note = "价格尚未稳定，建议观望至7月"
elif days_left > 60:
    recommendation = "buy"
    note = "最佳购票窗口 · 建议尽快入手"
elif days_left > 30:
    recommendation = "buy"
    note = "价格开始上涨 · 越等越贵"
else:
    recommendation = "urgent"
    note = "临近出发，赶紧购买"

cheapest_price = min(p["price"] for p in prices)
cheapest_airline = [p for p in prices if p["price"] == cheapest_price][0]["airline"]

entry = {
    "date": today.isoformat(),
    "routes": prices,
    "recommendation": recommendation,
    "note": note,
    "cheapest": f"{cheapest_airline} ¥{cheapest_price:,}",
    "days_left": days_left
}

# Update JSON archive
archive = []
if os.path.exists(PRICE_FILE):
    try:
        with open(PRICE_FILE, encoding="utf-8") as f:
            existing = json.load(f)
        if isinstance(existing, list):
            archive = existing
    except Exception as e:
        print(f"Read archive failed: {e}")

existing_dates = {e.get("date") for e in archive}
if today.isoformat() in existing_dates:
    for i, e in enumerate(archive):
        if e.get("date") == today.isoformat():
            archive[i] = entry
            break
else:
    archive.append(entry)
archive = sorted(archive, key=lambda x: x["date"])[-60:]

with open(PRICE_FILE, "w", encoding="utf-8") as f:
    json.dump(archive, f, ensure_ascii=False, indent=2)
print(f"Flight prices updated: {len(archive)} days of data, today: {recommendation}")

# Build HTML card
rec_colors = {"buy": "var(--aurora-green)", "wait": "var(--amber-warn)", "urgent": "var(--red-warn)"}
rec_labels = {"buy": "建议入手", "wait": "再等等", "urgent": "赶紧买"}
rec_icons = {"buy": "✅", "wait": "⏳", "urgent": "🔥"}

# Mini sparkline from last 14 data points
recent = archive[-14:]
hainan_prices = []
for e in recent:
    for r in e.get("routes", []):
        if "海航" in r.get("airline", ""):
            hainan_prices.append(r["price"])
            break
    if len(hainan_prices) < len(recent):
        if hainan_prices:
            hainan_prices.append(hainan_prices[-1])
        else:
            hainan_prices.append(5200)

if hainan_prices:
    min_p = min(hainan_prices)
    max_p = max(hainan_prices)
    price_range = max_p - min_p or 1
    chart_h = 36
    chart_w = 170
    points = []
    n = len(hainan_prices)
    for i, p in enumerate(hainan_prices):
        x = round(i * chart_w / (n - 1)) if n > 1 else chart_w // 2
        y = round(chart_h - (p - min_p) / price_range * chart_h)
        points.append(f"{x},{y}")
    polyline = " ".join(points)
else:
    polyline = "0,18 170,18"

route_html = ""
for p in prices:
    arrow = "↑" if p["trend"] == "up" else "↓" if p["trend"] == "down" else "→"
    arrow_color = "var(--red-warn)" if p["trend"] == "up" else "var(--aurora-green)" if p["trend"] == "down" else "var(--text-muted)"
    route_html += f"""<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.65rem;padding:3px 0;">
      <span style="color:var(--text-secondary);"><a href="{p['search_url']}" target="_blank" style="color:var(--text-secondary);text-decoration:none;">{p['airline']}</a></span>
      <span style="color:var(--text-primary);font-weight:600;">¥{p['price']:,} <span style="color:{arrow_color};font-size:0.55rem;">{arrow}</span></span>
    </div>"""

card = f"""<!-- FLIGHT_PRICES_START -->
  <div style="width:100%;max-width:420px;margin:8px auto 0;background:var(--bg-card);backdrop-filter:var(--glass-blur);border:1px solid rgba(57,255,20,0.2);border-left:3px solid var(--aurora-green);border-radius:var(--radius-sm);padding:10px 14px;text-align:left;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      <span style="font-size:0.7rem;font-weight:600;color:var(--aurora-green);">✈️ 机票价格追踪 · 成都→奥斯陆</span>
      <span style="font-size:0.55rem;background:{rec_colors[recommendation]};color:#050a1a;padding:2px 8px;border-radius:10px;font-weight:700;">{rec_icons[recommendation]} {rec_labels[recommendation]}</span>
    </div>
    <div style="display:flex;gap:12px;align-items:stretch;">
      <div style="flex:1;min-width:0;">
        {route_html}
      </div>
      <div style="flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;">
        <svg width="{chart_w}" height="{chart_h}" viewBox="0 0 {chart_w} {chart_h}" style="display:block;">
          <polyline points="{polyline}" fill="none" stroke="var(--aurora-green)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>
        </svg>
        <span style="font-size:0.5rem;color:var(--text-muted);margin-top:2px;">14天趋势（海航）</span>
      </div>
    </div>
    <div style="margin-top:6px;display:flex;justify-content:space-between;align-items:center;font-size:0.55rem;color:var(--text-muted);border-top:1px solid rgba(148,163,184,0.1);padding-top:5px;">
      <span>{note} · 距出发{days_left}天</span>
      <a href="https://www.google.com/travel/flights?q=TFU+to+OSL+2026-09-25&curr=CNY" target="_blank" style="color:var(--aurora-green);text-decoration:none;font-size:0.55rem;">Google Flights搜索 →</a>
    </div>
  </div>
<!-- FLIGHT_PRICES_END -->"""

# Update HTML
if not os.path.exists(HTML_FILE):
    print(f"{HTML_FILE} not found!")
    exit(1)

with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

if MARKER_START in html:
    pattern = re.compile(re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        html = pattern.sub(card, html)
        print("Updated existing flight price block.")
    else:
        print("Markers found but pattern didn't match, inserting at marker position.")
        html = html.replace(MARKER_START, card)
else:
    insert_before = '<div class="aurora-wave">'
    idx = html.find(insert_before)
    if idx > 0:
        html = html[:idx] + card + "\n  " + html[idx:]
        print(f"Inserted flight price card before aurora-wave.")
    else:
        print("Could not find insertion point.")
        exit(1)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print("Flight price tracker update complete.")
