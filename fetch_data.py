{
  "timestamp": "2026-04-16T17:49:34.160483+00:00",
  "date": "2026-04-16",
  "btc": {
    "price_usd": 102266.7,
    "change_24h_pct": 1.92,
    "market_cap_usd": 2014653990000
  },
  "composite": {
    "score": 33.9,
    "signal": "LONG",
    "verdict": "Les institutions accumulent",
    "weights_used": {
      "cot": 35,
      "oi": 20,
      "funding": 25,
      "etf": 20
    }
  },
  "sources": {
    "cot": {
      "label": "COT Report (Hedge Funds CME)",
      "score": 40.7,
      "available": true,
      "error": null,
      "weight": 35,
      "data": {
        "report_date": "2026-04-12",
        "long": 24580,
        "short": 18920,
        "net": 5660,
        "z_score": 0.84,
        "net_prev_week": 4210
      }
    },
    "oi": {
      "label": "Open Interest (Binance Futures)",
      "score": 41.6,
      "available": true,
      "error": null,
      "weight": 20,
      "data": {
        "oi_usd_now": 32400000000,
        "oi_change_7d_pct": 4.8,
        "price_change_7d_pct": 2.1,
        "interpretation": "Nouveaux longs (accumulation)"
      }
    },
    "funding": {
      "label": "Funding Rate (Perps)",
      "score": -17.1,
      "available": true,
      "error": null,
      "weight": 25,
      "data": {
        "current_rate_pct": 0.0095,
        "avg_7d_pct": 0.0078,
        "annualized_pct": 8.54,
        "regime": "Optimisme modéré"
      }
    },
    "etf": {
      "label": "Flux ETF Bitcoin Spot (US)",
      "score": 34.8,
      "available": true,
      "error": null,
      "weight": 20,
      "data": {
        "latest_date": "15 Apr 2026",
        "latest_flow_musd": 245.8,
        "cumulative_5d_musd": 892.3,
        "days_available": 10,
        "trend": "Entrées nettes"
      }
    }
  }
}