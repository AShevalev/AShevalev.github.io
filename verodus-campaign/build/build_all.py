"""Build every launch creative.

    python3 build_all.py

Outputs 1080-wide PNGs to ads/meta/creatives/launch/.
Requires: google-chrome (headless) and the Inter font family.
"""

import week1
import week2
import week3
import week4

for label, mod in [("Week 1 — Launch & free trial", week1),
                   ("Week 2 — Rules & transparency", week2),
                   ("Week 3 — Trust & first cohort", week3),
                   ("Week 4 — Founding offer", week4)]:
    print(f"\n{label}")
    mod.build()
