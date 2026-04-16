"""Génère un latest.json + history.json avec des données démo réalistes."""
import json, math, random
from datetime import datetime, timezone, timedelta
from pathlib import Path

random.seed(42)
DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)

now = datetime.now(timezone.utc)

# Génère 90 jours d'historique avec une tendance réaliste
history = []
score = -15.0
for i in range(90, 0, -1):
    d = now - timedelta(days=i)
    # Random walk avec tendance
    score += random.gauss(0.3, 8)
    score = max(-85, min(85, score))
    price = 95000 + math.sin(i / 10) * 8000 + random.gauss(0, 1500) + (90 - i) * 100

    signal = "LONG" if score >= 30 else ("SHORT" if score <= -30 else "NEUTRE")
    history.append({
        "date": d.strftime("%Y-%m-%d"),
        "timestamp": d.isoformat(),
        "composite_score": round(score, 1),
        "signal": signal,
        "btc_price": round(price, 2),
        "cot_score": round(score + random.gauss(0, 10), 1),
        "oi_score": round(score * 0.7 + random.gauss(0, 15), 1),
        "funding_score": round(-score * 0.5 + random.gauss(0, 20), 1),
        "etf_score": round(score * 1.2 + random.gauss(0, 12), 1),
    })

# Dernier snapshot
last = history[-1]
latest = {
    "timestamp": now.isoformat(),
    "date": now.strftime("%Y-%m-%d"),
    "btc": {
        "price_usd": last["btc_price"],
        "change_24h_pct": round(random.uniform(-3, 3), 2),
        "market_cap_usd": int(last["btc_price"] * 19_700_000),
    },
    "composite": {
        "score": last["composite_score"],
        "signal": last["signal"],
        "verdict": (
            "Les institutions accumulent" if last["signal"] == "LONG"
            else "Les institutions distribuent" if last["signal"] == "SHORT"
            else "Positionnement indécis"
        ),
        "weights_used": {"cot": 35, "oi": 20, "funding": 25, "etf": 20},
    },
    "sources": {
        "cot": {
            "label": "COT Report (Hedge Funds CME)",
            "score": last["cot_score"],
            "available": True, "error": None, "weight": 35,
            "data": {
                "report_date": (now - timedelta(days=4)).strftime("%Y-%m-%d"),
                "long": 24580, "short": 18920,
                "net": 5660, "z_score": 0.84,
                "net_prev_week": 4210,
            },
        },
        "oi": {
            "label": "Open Interest (Binance Futures)",
            "score": last["oi_score"],
            "available": True, "error": None, "weight": 20,
            "data": {
                "oi_usd_now": 32_400_000_000,
                "oi_change_7d_pct": 4.8,
                "price_change_7d_pct": 2.1,
                "interpretation": "Nouveaux longs (accumulation)",
            },
        },
        "funding": {
            "label": "Funding Rate (Perps)",
            "score": last["funding_score"],
            "available": True, "error": None, "weight": 25,
            "data": {
                "current_rate_pct": 0.0095,
                "avg_7d_pct": 0.0078,
                "annualized_pct": 8.54,
                "regime": "Optimisme modéré",
            },
        },
        "etf": {
            "label": "Flux ETF Bitcoin Spot (US)",
            "score": last["etf_score"],
            "available": True, "error": None, "weight": 20,
            "data": {
                "latest_date": (now - timedelta(days=1)).strftime("%d %b %Y"),
                "latest_flow_musd": 245.8,
                "cumulative_5d_musd": 892.3,
                "days_available": 10,
                "trend": "Entrées nettes",
            },
        },
    },
}

(DATA / "latest.json").write_text(json.dumps(latest, indent=2, ensure_ascii=False))
(DATA / "history.json").write_text(json.dumps(history, indent=2, ensure_ascii=False))
print(f"✅ Démo générée : signal={last['signal']} ({last['composite_score']})")
