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
| `write_reprice_pdf.py` | News-included reprice (more leftover, still under peers) → `results/Verodus_Reprice_News_Included_2026-08-17.pdf` |
| `competitor_addons.py` | 19-peer checkout add-ons + leftover vs rec → `results/COMPETITOR_ADDONS.md` |
| `write_addon_analysis_pdf.py` | Competitor add-on analysis + why Verodus rec → `results/Verodus_Addon_Competitor_Analysis_2026-08-17.pdf` |
| `write_addon_combo_pdf.py` | BE, margins, leftover for every legal add-on cart → `results/Verodus_Addon_BE_Margins_2026-08-17.pdf` |
| `run_news_included.py` | News allowed on all phases (not an add-on) → `results/Verodus_News_Included_2026-08-17.pdf` |
| `write_complete_report.py` | One operator report (P(pay) audit + BE $ + margins) → `results/Verodus_Complete_Report_2026-08-16.pdf` |
| `write_confirmed_book.py` | Confirmed summary + all rank / industry / rec tables → `results/Verodus_Confirmed_Book_2026-08-16.pdf` |
| `write_challenge_catalog.py` | Shopper catalog (rec sale + list, Lite funded 8%) → `results/Verodus_Challenge_Catalog_2026-08-17.pdf` |
| `write_simple_catalogs.py` | Simple PDFs: plans+rules, pricing catalogue, add-on %, BE/20/40/60/Sale m |
| `write_be_margin_card.py` | Challenge + add-on BE, 20%, 40%, 60%, Sale m on the 17 Aug card |
| `write_addon_catalog.py` | Add-on % + stickers per SKU → `results/Verodus_Addon_Catalog_2026-08-17.pdf` |
| `write_addon_pct_pdf.py` | Profitable-but-competitive add-on % + BE leftover → `results/Verodus_Addon_Pct_BE_2026-08-17.pdf` |
| `write_new_pack.py` | Margins PDF + catalog (prices, rules, add-on %) on the 17 Aug card |
| `write_book_310.py` | 310-account monthly P&L (wages CAD 10k, leftover after opex) |
| `verodus_mc.py` | Verodus-only engine (FAQ rules) |
| `run_fundedhive.py` | FundedHive print / BE → `results/FUNDEDHIVE.md` + CSVs |
| `write_fundedhive_pdf.py` | FundedHive print/BE card → `results/FundedHive_Print_BE_2026-08-21.pdf` |
| `write_vh_compare_pdf.py` | Verodus vs FundedHive side-by-side → `results/Verodus_vs_FundedHive_2026-08-21.pdf` + 1-page scoreboard |
