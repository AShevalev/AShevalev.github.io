# Prop-firm Monte Carlo

Industry-calibrated book (7/22/26/28/17) plus the live Verodus FAQ book.

```bash
pip install -r sim/requirements.txt

# Top-20 catalog + Verodus (writes results/INDUSTRY_REPORT.md)
PYTHONPATH=sim python sim/run_industry.py --n-sims 1000

# Verodus-only (writes results/REPORT.md)
PYTHONPATH=sim python sim/run.py --n-sims 4000
```

| File | What |
|---|---|
| `industry_book.py` | Calibrated profiles + engine |
| `catalog.py` | 20 firms, 47 products, list/sale prices |
| `run_industry.py` | Catalog runner (`--only` + `--merge` to refresh one product) |
| `write_comprehensive_pdf.py` | Industry PDF → `results/Verodus_Industry_Report_2026-08-16.pdf` |
| `difficulty.py` | Numeric D (0–100) per plan; compare only if same family + size and \|ΔD\| ≤ 6 |
| `write_rank_report.py` | D + 20%/30% rank inside the ±6 band → `results/Verodus_BE_Rank_Report_2026-08-16.pdf` |
| `write_price_rec_pdf.py` | Attractive VERO35 card vs family street → `results/Verodus_Recommended_Prices_2026-08-16.pdf` |
| `write_complete_report.py` | One operator report (P(pay) audit + BE $ + margins) → `results/Verodus_Complete_Report_2026-08-16.pdf` |
| `verodus_mc.py` | Verodus-only engine (FAQ rules) |
| `run.py` | Verodus-only runner |
