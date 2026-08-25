# Organisation structure

**As of 25 August 2026.** Three companies. None is a parent or subsidiary of another. Shareholding is personal.

Printed visual: open `org-chart.html` and export to PDF.

## Ownership

```text
              Kim Chen                         Chun Chan
         100% shareholder                 100% shareholder
            |            |                       |
  Verodus Capital   Verodus L.L.C.-FZ     1591011 B.C. Ltd.
  British Columbia  Meydan FZ, Dubai      British Columbia
```

| Company | Jurisdiction | Shareholder | What it does |
| --- | --- | --- | --- |
| **Verodus Capital Inc.** | British Columbia, Canada | **Kim Chen — 100%** | Marketing and traffic to the domain. Payment processing on its own merchant accounts. Evaluations for its own reward decisions. Does not provide KYC. |
| **Verodus L.L.C.-FZ** | Meydan Free Zone, Dubai, UAE | **Kim Chen — 100%** | Owns `verodus.com`. Domain and hosting are in the UAE. Owns raw data and KYC records. Performs all KYC of domain users. Runs the CRM and dashboard. |
| **1591011 B.C. Ltd.** | British Columbia, Canada | **Chun Chan — 100%** (investor in Verodus) | Owns the proprietary software, CRM, and related technology. Kim Chen developed the software for 1591011 B.C. Ltd. Sublicenses the system to Verodus L.L.C.-FZ. |

Verodus Capital Inc. and Verodus L.L.C.-FZ are affiliates (same 100% shareholder). 1591011 B.C. Ltd. is owned by Chun Chan, who is one of the investors in Verodus. Kim Chen developed the software for 1591011 B.C. Ltd. The three companies deal with each other by contract, not by corporate control.

## People

Marketing sits with Capital. David was in-house from April until June; wages for those two months were $8,000. He returns part-time next month for marketing. An intern is expected at approximately $3,000 a month for marketing and customer support.

## Who holds what

| Question | Answer |
| --- | --- |
| Who owns Verodus Capital Inc.? | Kim Chen, 100%. |
| Who owns Verodus L.L.C.-FZ? | Kim Chen, 100%. |
| Who owns 1591011 B.C. Ltd.? | Chun Chan, 100%. Chun Chan is one of the investors in Verodus. |
| Who developed the software? | Kim Chen, for 1591011 B.C. Ltd. |
| Who owns the domain? | Verodus L.L.C.-FZ (`verodus.com`). Domain and hosting are in the UAE. Stack: Vercel on AWS (including Lambda), email, website, database, Redis. |
| Who holds the data? | Verodus L.L.C.-FZ owns raw data, client-identifying information, and KYC records. Aggregated insights are licensed to 1591011 B.C. Ltd. |
| Who performs KYC? | Verodus L.L.C.-FZ, in its own name. Capital and 1591011 do not provide KYC. |
| Who owns the system? | 1591011 B.C. Ltd. Dubai’s right is a limited, revocable, non-transferable licence. Dubai cannot sublicense. |
| Where does money land? | Verodus Capital Inc., on merchant accounts in Capital’s name. Canadian tax is filed on Capital. |

## Contracts among these three

- Software licence (31 May 2026): 1591011 B.C. Ltd. ↔ Verodus L.L.C.-FZ. No cash. Title to the software stays with 1591011. KYC is LLC-FZ’s.
- Operational services, domain usage and evaluation rights (28 April 2026): Verodus Capital Inc. ↔ Verodus L.L.C.-FZ. Marketing and traffic; Capital does not provide KYC. Isolated payment rails. Optional 5% royalty. VanIAC arbitration.

Both agreements can be varied in writing if this endeavour requires it.
