"""
BTC Institutional Radar - Data Fetcher
Récupère les données de positionnement institutionnel et calcule un score composite.

Sources :
  1. CFTC COT Report (positions hedge funds sur CME BTC futures)
  2. Binance/Coinglass (Open Interest + Funding Rates)
  3. Farside Investors (flux ETF Bitcoin spot US)
  4. CoinGecko (prix BTC de référence)
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

# ─── CONFIG ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
HISTORY_FILE = DATA_DIR / "history.json"
LATEST_FILE = DATA_DIR / "latest.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

WEIGHTS = {"cot": 35, "oi": 20, "funding": 25, "etf": 20}
LONG_THRESHOLD = 30
SHORT_THRESHOLD = -30


@dataclass
class SourceResult:
    score: float       # -100 à +100
    raw: dict[str, Any]
    label: str
    available: bool = True
    error: str | None = None


# ─── 1. COT REPORT ───────────────────────────────────────────────────
def fetch_cot() -> SourceResult:
    """
    CFTC Commitments of Traders — Bitcoin CME futures (code 133741).
    On cible les 'Leveraged Funds' qui sont le meilleur proxy des hedge funds.
    API Socrata publique, pas besoin de clé.
    """
    try:
        url = (
            "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
            "?cftc_contract_market_code=133741"
            "&$order=report_date_as_yyyy_mm_dd DESC"
            "&$limit=60"
        )
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        rows = r.json()
        if not rows:
            return SourceResult(0, {}, "COT", False, "Aucune donnée")

        # Position nette = longs - shorts (Leveraged Funds)
        def net(row):
            return (
                float(row.get("lev_money_positions_long_all", 0) or 0)
                - float(row.get("lev_money_positions_short_all", 0) or 0)
            )

        nets = [net(row) for row in rows]
        latest = nets[0]

        # Z-score sur 52 semaines (si dispo)
        window = nets[: min(52, len(nets))]
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std = math.sqrt(variance) if variance > 0 else 1
        z = (latest - mean) / std

        # Tanh-like scaling vers [-100, +100]
        score = 100 * (2 / (1 + math.exp(-z)) - 1)

        return SourceResult(
            score=round(score, 1),
            raw={
                "report_date": rows[0].get("report_date_as_yyyy_mm_dd", "")[:10],
                "long": int(float(rows[0].get("lev_money_positions_long_all", 0) or 0)),
                "short": int(float(rows[0].get("lev_money_positions_short_all", 0) or 0)),
                "net": int(latest),
                "z_score": round(z, 2),
                "net_prev_week": int(nets[1]) if len(nets) > 1 else None,
            },
            label="COT Report (Hedge Funds CME)",
        )
    except Exception as exc:
        return SourceResult(0, {}, "COT", False, str(exc))


# ─── 2. OPEN INTEREST ────────────────────────────────────────────────
def fetch_open_interest() -> SourceResult:
    """
    Open Interest agrégé via l'API publique Binance Futures.
    On regarde la variation 7j de l'OI croisée avec la direction du prix.
      - OI ↑ + Prix ↑  = nouveaux longs (bullish)
      - OI ↑ + Prix ↓  = nouveaux shorts (bearish)
      - OI ↓ + Prix ↑  = short squeeze (bullish mais fragile)
      - OI ↓ + Prix ↓  = longs qui capitulent (bearish mais terminal)
    """
    try:
        url = "https://fapi.binance.com/futures/data/openInterestHist"
        params = {"symbol": "BTCUSDT", "period": "1d", "limit": 8}
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        rows = r.json()
        if len(rows) < 2:
            return SourceResult(0, {}, "OI", False, "Données insuffisantes")

        oi_now = float(rows[-1]["sumOpenInterestValue"])
        oi_prev = float(rows[0]["sumOpenInterestValue"])
        oi_change_pct = (oi_now - oi_prev) / oi_prev * 100

        price_now = float(rows[-1]["sumOpenInterest"]) and \
                    float(rows[-1]["sumOpenInterestValue"]) / float(rows[-1]["sumOpenInterest"])
        price_prev = float(rows[0]["sumOpenInterest"]) and \
                     float(rows[0]["sumOpenInterestValue"]) / float(rows[0]["sumOpenInterest"])
        price_change_pct = (price_now - price_prev) / price_prev * 100

        raw_score = oi_change_pct * (1 if price_change_pct >= 0 else -1)
        score = max(-100, min(100, raw_score * 4))  # amplification raisonnable

        return SourceResult(
            score=round(score, 1),
            raw={
                "oi_usd_now": int(oi_now),
                "oi_change_7d_pct": round(oi_change_pct, 2),
                "price_change_7d_pct": round(price_change_pct, 2),
                "interpretation": _oi_interpretation(oi_change_pct, price_change_pct),
            },
            label="Open Interest (Binance Futures)",
        )
    except Exception as exc:
        return SourceResult(0, {}, "OI", False, str(exc))


def _oi_interpretation(oi_chg: float, price_chg: float) -> str:
    if oi_chg > 0 and price_chg > 0:
        return "Nouveaux longs (accumulation)"
    if oi_chg > 0 and price_chg < 0:
        return "Nouveaux shorts (pression vendeuse)"
    if oi_chg < 0 and price_chg > 0:
        return "Short squeeze (couverture)"
    return "Capitulation longs (désengagement)"


# ─── 3. FUNDING RATE ─────────────────────────────────────────────────
def fetch_funding() -> SourceResult:
    """
    Funding rate historique Binance BTCUSDT perpetual.
    Logique contrarian : funding très positif = retail euphorique = souvent top local.
    Moyenne sur 7 jours (21 périodes de 8h).
    """
    try:
        url = "https://fapi.binance.com/fapi/v1/fundingRate"
        params = {"symbol": "BTCUSDT", "limit": 21}
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        rows = r.json()
        if not rows:
            return SourceResult(0, {}, "Funding", False, "Aucune donnée")

        rates = [float(row["fundingRate"]) for row in rows]
        avg = sum(rates) / len(rates)
        latest = rates[-1]

        # Funding moyen typique : ~0.0001 (0.01% par 8h). Extrêmes : ±0.001.
        # On inverse : funding haut = score négatif (retail trop long)
        score = max(-100, min(100, -avg * 100000))

        return SourceResult(
            score=round(score, 1),
            raw={
                "current_rate_pct": round(latest * 100, 4),
                "avg_7d_pct": round(avg * 100, 4),
                "annualized_pct": round(avg * 3 * 365 * 100, 2),
                "regime": _funding_regime(avg),
            },
            label="Funding Rate (Perps)",
        )
    except Exception as exc:
        return SourceResult(0, {}, "Funding", False, str(exc))


def _funding_regime(avg: float) -> str:
    if avg > 0.0003:
        return "Euphorie retail (contrarian bearish)"
    if avg > 0.0001:
        return "Optimisme modéré"
    if avg > -0.0001:
        return "Neutre"
    if avg > -0.0003:
        return "Pessimisme (accumulation possible)"
    return "Peur extrême (contrarian bullish)"


# ─── 4. FLUX ETF SPOT (Farside) ──────────────────────────────────────
def fetch_etf_flows() -> SourceResult:
    """
    Scrape Farside Investors pour les flux nets ETF Bitcoin spot US.
    Tous les flux en millions de $ par jour.
    Le site publie un tableau HTML assez stable.
    """
    try:
        url = "https://farside.co.uk/bitcoin-etf-flow-all-data/"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        html = r.text

        # On cherche les lignes de données — Farside utilise un tableau simple
        # Pattern : date puis colonnes de nombres, la dernière = Total
        # On parse en cherchant le total "Total" column par ligne
        rows = re.findall(
            r'<tr[^>]*>\s*<td[^>]*>(\d{2}\s\w{3}\s\d{4})</td>(.*?)</tr>',
            html,
            re.DOTALL,
        )
        if not rows:
            return SourceResult(0, {}, "ETF", False, "Parser: aucune ligne trouvée")

        flows = []
        for date_str, cells_html in rows[:10]:  # 10 derniers jours ouvrés
            cells = re.findall(r'<td[^>]*>(.*?)</td>', cells_html, re.DOTALL)
            if not cells:
                continue
            total_raw = re.sub(r'<[^>]+>', '', cells[-1]).strip()
            total_raw = total_raw.replace(",", "").replace("(", "-").replace(")", "")
            try:
                total = float(total_raw)
                flows.append({"date": date_str, "flow_musd": total})
            except ValueError:
                continue

        if not flows:
            return SourceResult(0, {}, "ETF", False, "Parser: aucun flux numérique")

        # Score : somme des flux sur 5j / volatilité typique (±500M/j)
        recent = flows[:5]
        total_5d = sum(f["flow_musd"] for f in recent)
        # Un flux cumulé 5j de +2500M = fort long, -2500M = fort short
        score = max(-100, min(100, total_5d / 25))

        return SourceResult(
            score=round(score, 1),
            raw={
                "latest_date": flows[0]["date"],
                "latest_flow_musd": round(flows[0]["flow_musd"], 1),
                "cumulative_5d_musd": round(total_5d, 1),
                "days_available": len(flows),
                "trend": "Entrées nettes" if total_5d > 0 else "Sorties nettes",
            },
            label="Flux ETF Bitcoin Spot (US)",
        )
    except Exception as exc:
        return SourceResult(0, {}, "ETF", False, str(exc))


# ─── 5. PRIX BTC (contexte) ──────────────────────────────────────────
def fetch_btc_price() -> dict:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
        }
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()["bitcoin"]
        return {
            "price_usd": round(data["usd"], 2),
            "change_24h_pct": round(data.get("usd_24h_change", 0), 2),
            "market_cap_usd": int(data.get("usd_market_cap", 0)),
        }
    except Exception:
        return {"price_usd": None, "change_24h_pct": None, "market_cap_usd": None}


# ─── COMPOSITE ───────────────────────────────────────────────────────
def compute_composite(sources: dict[str, SourceResult]) -> dict:
    total_weight = 0
    weighted_sum = 0
    for key, weight in WEIGHTS.items():
        src = sources.get(key)
        if src and src.available:
            weighted_sum += src.score * weight
            total_weight += weight

    composite = weighted_sum / total_weight if total_weight > 0 else 0

    if composite >= LONG_THRESHOLD:
        signal = "LONG"
        verdict = "Les institutions accumulent"
    elif composite <= SHORT_THRESHOLD:
        signal = "SHORT"
        verdict = "Les institutions distribuent"
    else:
        signal = "NEUTRE"
        verdict = "Positionnement indécis"

    return {
        "score": round(composite, 1),
        "signal": signal,
        "verdict": verdict,
        "weights_used": {k: WEIGHTS[k] for k, s in sources.items() if s.available},
    }


# ─── MAIN ────────────────────────────────────────────────────────────
def main() -> int:
    print("🔍 BTC Institutional Radar — fetching data...")
    DATA_DIR.mkdir(exist_ok=True)

    print("  [1/4] COT Report...")
    cot = fetch_cot()
    print(f"        → score={cot.score} ({'OK' if cot.available else cot.error})")

    print("  [2/4] Open Interest...")
    oi = fetch_open_interest()
    print(f"        → score={oi.score} ({'OK' if oi.available else oi.error})")

    print("  [3/4] Funding Rate...")
    fund = fetch_funding()
    print(f"        → score={fund.score} ({'OK' if fund.available else fund.error})")

    print("  [4/4] ETF Flows...")
    etf = fetch_etf_flows()
    print(f"        → score={etf.score} ({'OK' if etf.available else etf.error})")

    print("  [+] BTC Price...")
    price = fetch_btc_price()

    sources = {"cot": cot, "oi": oi, "funding": fund, "etf": etf}
    composite = compute_composite(sources)

    now = datetime.now(timezone.utc)
    snapshot = {
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "btc": price,
        "composite": composite,
        "sources": {
            key: {
                "label": src.label,
                "score": src.score,
                "available": src.available,
                "error": src.error,
                "data": src.raw,
                "weight": WEIGHTS[key],
            }
            for key, src in sources.items()
        },
    }

    # Sauvegarde 'latest'
    LATEST_FILE.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))

    # Append à l'historique (dédupliqué par date)
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text())
        except Exception:
            history = []

    history = [h for h in history if h.get("date") != snapshot["date"]]
    history.append({
        "date": snapshot["date"],
        "timestamp": snapshot["timestamp"],
        "composite_score": composite["score"],
        "signal": composite["signal"],
        "btc_price": price.get("price_usd"),
        "cot_score": cot.score if cot.available else None,
        "oi_score": oi.score if oi.available else None,
        "funding_score": fund.score if fund.available else None,
        "etf_score": etf.score if etf.available else None,
    })
    history.sort(key=lambda x: x["date"])
    history = history[-365:]  # Garde 1 an max

    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False))

    print()
    print(f"✅ Done — Signal: {composite['signal']} (score: {composite['score']})")
    print(f"   Saved to {LATEST_FILE.relative_to(ROOT)}")
    print(f"   History: {len(history)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
