# Verodus organisation structure

Prepared for Joe M. Wong following the 25 August 2026 call. This describes **current** legal entities and roles as they stand in the signed agreements and as described on the call. Shareholding percentages and beneficial ownership are **not** in the three agreements; those still need to be confirmed in a cap-table annex.

Legal name of the group: **Verodus** (not Veritis / Veritus).

## Snapshot

| Entity | Jurisdiction | Signatory on file | What it actually does |
| --- | --- | --- | --- |
| **1591011 B.C. Ltd.** | British Columbia, Canada | Chun Chan, Director | Owns the proprietary software, CRM, and related technology. Grants Dubai a limited sublicense. Receives a licence back to **aggregated insights** only. |
| **Verodus Holding Inc.** | Canada (agreement governed by BC law) | Kim Chen, Director | Holds **third-party** software licence agreements and sublicenses those products to Dubai on the same data-licence-back pattern. |
| **Verodus Capital Inc.** | British Columbia, Canada | Kim Chen, Director | Current **profit centre**. Independent payment processing (pay-ins, rewards, refunds, banking) on its own merchant accounts. Marketing, traffic, KYC support. Licensed to use `verodus.com`. |
| **Verodus L.L.C.-FZ** | Meydan Free Zone, Dubai, UAE | Kim Chen, Manager | Owns **verodus.com**. Collects and **owns raw data** (including client-identifying data). Runs CRM / dashboard. Isolated merchant accounts on paper (not the processor currently in use). Meydan activities: IT consultancy; management consultancy; data classification and analysis. |

**People named on the call (not a full cap table)**

- **Kim Chen** — Director / CEO as described on the call; Manager of the Dubai FZ company; Director of Holding and of Capital; sole IT / automation person.
- **Chun Chan** — Director of 1591011 B.C. Ltd., the company that owns the proprietary system. On the call this was described as the investor-held British Columbia white-label company.
- **Alexander** — commercial / operating counterpart on the call; will confirm executive roster, employees vs contractors, and investor list in a follow-up annex.
- Current marketing capacity described on the call: one content creator (company, not freelance agency); one intern nearly onboard for support and content.

## How work is split today

```text
                         INVESTORS / HOLDERS
                    (percentages to be annexed)
          ┌─────────────────┬─────────────────┬─────────────────┐
          ▼                 ▼                 ▼                 ▼
   1591011 B.C. Ltd.  Verodus Holding   Verodus Capital   Verodus L.L.C.-FZ
   Proprietary         Third-party       Canada profit     Dubai operating
   software / CRM      software          centre            company
          │            licences                │                  │
          │ sublicense (no cash)               │                  │
          └────────────────┬───────────────────┘                  │
                           ▼                                      │
                    Verodus L.L.C.-FZ  ◄── domain + raw data ─────┘
                    verodus.com
                    CRM / dashboard / data collection
                           │
                           │ domain + evaluation licence
                           ▼
                    Verodus Capital Inc.
                    marketing + KYC support
                    payment processing (Canada rails in use)
                    ~95% of receipts today;
                    Dubai may levy 5% royalty
```

## Who holds what Joe asked about

| Question Joe asked | Current answer |
| --- | --- |
| Who owns the domain? | Verodus L.L.C.-FZ (`verodus.com`). |
| Who collects / holds data? | Verodus L.L.C.-FZ owns **raw** data and client-identifying information. Aggregated, anonymised insights are licensed to 1591011 B.C. Ltd. and to Verodus Holding Inc. |
| Who runs the CRM / dashboard? | Verodus L.L.C.-FZ. |
| Who owns the system / white label? | **1591011 B.C. Ltd.** owns the proprietary software. Dubai’s right is a **non-exclusive, non-transferable, revocable** sublicense. Dubai **cannot re-sublicense** to anyone else. |
| Who is the profit centre / where does money land? | **Verodus Capital Inc. (Canada)** today. A UAE processor exists but is not used. |
| Who does sales and marketing? | Capital is contracted to drive traffic to the domain and provide marketing. In practice this is in-house (one content creator; intern joining). |
| Who does KYC? | Capital provides KYC verification support to Dubai. |
| How are the companies held? | **Not in the three agreements.** Needs a share register / cap-table annex (personal vs corporate holders, percentages). |
| Where is it hosted (AWS, etc.)? | **Not in the three agreements.** To be confirmed with Kim (region, provider, who is the cloud account holder). |
| Which company should Joe sign with? | Not decided. Joe’s legal team will pick after reading this chart. TradeMap is Joe’s intended commercial vehicle for the TAMS integration. |

## Joe’s side (for context, not Verodus entities)

| Entity | Role Joe described |
| --- | --- |
| TradeMap | Education, mentorship, small-lump funding; contract party for TAMS. |
| MoneyMap | Real-money / fund management for approved traders. |
| World Trader Hub (Hong Kong) | Public-facing organisation / non-profit positioning and network. |
| TAMS | Technical product to integrate with Verodus’s backend. |

## Intercompany economics (short)

- Software sublicenses (Holding → Dubai, 31 May 1591011 → Dubai): **no invoices, no cash.** Consideration is reciprocal licences.
- Capital ↔ Dubai operational agreement: **no invoices by default.** Dubai may, at its **sole discretion** and on **90 days’ notice**, charge Capital a **5% royalty on gross sales (CAD)**, paid quarterly. That matches the “95% / 5% discretionary royalty” description on the call.
- Capital and Dubai must keep **separate** merchant accounts. No commingling.
- Each of the three agreements is written as **independent** of the others. Term on each: **36 months** from its effective date, BC law, BCICAC arbitration in Vancouver.

Printed visual: open `org-chart.html` and export to PDF.
