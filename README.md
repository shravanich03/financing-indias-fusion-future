# Financing India's Fusion Future

**Assessing bankability, investment risk and policy pathways for commercial fusion in India, 2026–2050.**

![Dashboard](docs/dashboard.png)

> **Illustrative model.** No commercial fusion plant exists today. The 10 plants are *modelled*, placed at real NPCIL nuclear-site locations, and are **not announced projects**. Every input is either sourced or a clearly labelled assumption (see [`assumptions_register.csv`](assumptions_register.csv)).

**Live interactive web version:** [shravanich03.github.io/financing-indias-fusion-future](https://shravanich03.github.io/financing-indias-fusion-future/) *(Chart.js build of the same model; the main dashboard is in Power BI)*

---

## The question
If commercial fusion became available in India, could its first plants be financed by lenders who require a **minimum 1.30x debt-service coverage ratio (DSCR)**, and what would it take to make them bankable?

## Key findings (constant-2026 ₹)

| Scenario | Investment | Generation 2050 | Avg project IRR | DSCR ≥ 1.30x | Fully bankable |
|---|---|---|---|---|---|
| Conservative | ₹6.34 L Cr | 33 TWh | 4.42% | 0 of 10 | 0 of 10 |
| **Base** | **₹5.28 L Cr** | **62 TWh** | **7.21%** | **6 of 10** | **3 of 10** |
| Accelerated | ₹4.49 L Cr | 65 TWh | 9.37% | 9 of 10 | 8 of 10 |

1. **Cost learning drives bankability.** The first plant (Kalpakkam, 2044) has a minimum DSCR of **0.77x**. The last (Haripur, 2050) reaches **1.80x** with an 86% Monte Carlo pass rate.
2. **Two different tests.** 6 of 10 plants clear the 1.30x covenant on base-case numbers, but only 3 are *fully bankable*: they must also clear it in at least 70% of 5,000 correlated simulations.
3. **Support changes the outcome.** Plants clearing 1.30x rise from 6 (no support) to 9 with a 20–30% viability-gap grant or 6.5% concessional debt, and to all 10 with 30% VGF plus 6.5% debt. *These levers are hypothetical; no fusion-specific support exists today.*
4. **FX risk is manageable.** On the 22% foreign-currency tranche, portfolio average minimum DSCR moves only from 1.36x to 1.31x under a 20% rupee fall.
5. **Scale check.** The 8.5 GW pipeline costs ₹5.28 L Cr, roughly 28% of the ~₹19 L Cr estimated for India's whole 100 GW nuclear target.

## What the dashboard shows
- **KPI cards:** investment, 2050 generation, average IRR, average risk, plants meeting the DSCR covenant, fully bankable plants.
- **Risk vs bankability scatter,** capacity by state, and the capital stack by instrument.
- **Portfolio table** with colour-coded risk, DSCR and bankability status.
- **Monte Carlo** probability of meeting the covenant, and risk contribution by dimension.
- **Generation by scenario** and the **policy levers** chart.
- **Interactive controls:** Scenario and State slicers, plus sidebar buttons (bookmarks) that switch scenarios and states.

## Method
- **Capex:** first-plant cost of $8,500/kW at ₹95.5/USD, a **12% learning rate per doubling of cumulative capacity**, a site/EPC factor, and **interest during construction (IDC)** added.
- **Basis:** all figures in **constant-2026 ₹**, with debt at the real rate, (1 + 9%) / (1 + 4.5%) − 1 ≈ 4.3%.
- **Financing:** 65% gearing, 18-year annuity debt, 22% of debt in foreign currency, 25.17% tax.
- **Revenue:** real tariff of ₹11.5/kWh, capacity factors of 78–90%, and an 80% first-year ramp-up. DSCR is tested in the ramp-up year, the binding year.
- **Scenarios:** Conservative / Base / Accelerated vary capex, tariff, capacity factor and commissioning date.
- **Risk score:** six weighted dimensions: technology maturity, regulation, fuel supply, construction, offtake and grid evacuation.
- **Monte Carlo:** 5,000 draws per project, with a common factor linking capex overruns, tariff shocks, capacity factor and delay.
- **Bankable status:** *Bankable* = DSCR ≥ 1.30x **and** P(DSCR ≥ 1.30x) ≥ 70%. *Marginal* = DSCR ≥ 1.15x or P ≥ 40%. Otherwise *Not Bankable*.

## Policy context
- The **SHANTI Act 2025** repealed the Atomic Energy Act 1962 and the Civil Liability for Nuclear Damage Act 2010, opened nuclear power to private participation, and supports a 100 GW by 2047 target. Sources: [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en-be/knowledge/publications/dbff80e4/shanti-act-2025-rewiring-india-s-nuclear-liability-and-regulatory-architecture) and [Power Line](https://powerline.net.in/2026/02/05/nuclear-power-reforms-shanti-act-2025-opens-the-doors-for-private-sector-participation/).
- The ~₹19 lakh crore estimate for the 100 GW target comes from [Inc42](https://inc42.com/resources/indias-nuclear-revolution-has-restarted-rd-must-follow-fast/).
- *Whether the SHANTI Act covers fusion specifically has not been verified. Read the Act's definitions before relying on it.*

## Limitations
- Tariff, first-plant capex, learning rate and operating cost are **assumptions**, not observed data. The tariff represents a "firm clean power" premium.
- The 12% learning rate is a single assumption and has not been sensitivity-tested.
- Offtake and grid risk scores by state are **illustrative**. Replace them with Ministry of Power DISCOM ratings.
- Real-terms DSCR is slightly kinder in early years than a nominal annuity schedule would be.
- Policy levers are hypothetical.

## Repository
```
model.py                  financial model, Monte Carlo and policy levers  -> data/
export_powerbi.py         builds the Power BI-ready tables                 -> powerbi/
assumptions_register.csv  every input, with its source and status
data/                     model outputs
powerbi/                  data tables, theme, canvas background, DAX measures, build guide
docs/                     dashboard screenshot and the interactive web version
```
**Reproduce:**
```bash
pip install -r requirements.txt
python model.py
python export_powerbi.py
```
Then follow [`powerbi/COMPLETE_BUILD_GUIDE.md`](powerbi/COMPLETE_BUILD_GUIDE.md) (canvas 1920 × 1480) and use the measures in [`powerbi/fusion_all_measures.txt`](powerbi/fusion_all_measures.txt).

## Tools
Python (NumPy, pandas) · Power BI (DAX, bookmarks, conditional formatting) · Chart.js

---
**Author:** Shravani Chavan · [GitHub](https://github.com/shravanich03) · [LinkedIn](https://www.linkedin.com/in/shravani-chavan-)
© 2026 Shravani Chavan. All rights reserved. Shared for viewing and portfolio purposes.
