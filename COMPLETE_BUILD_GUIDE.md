# Complete Power BI Build Guide — Financing India's Fusion Future
Canvas: **1920 × 1080 px** · Work in **Power BI Desktop** (free, Windows). Every phase ends with a CHECK. Do not continue until the check passes.
Files (all in the `powerbi` folder): canvas_background_1920x1080.png · fusion_theme.json · 6 CSVs · fusion_all_measures.dax

---
## PHASE 1 — Canvas and theme (10 min)
1. Open Power BI Desktop > blank report.
2. Click on empty canvas. Open the **Format page** pane (paint-roller icon) > **Canvas settings** > Type = **Custom**, Width **1920**, Height **1080**.
3. Same pane > **Canvas background** > Browse > `canvas_background_1920x1080.png` > Image fit = **Fit** > Transparency **0%**.
4. **Wallpaper** section (below) > Colour `#07111D`, transparency 0%.
5. View tab > Page view > **Fit to page** (zoom is only your viewing level; ignore the % shown).
6. View > Themes dropdown > **Browse for themes** > `fusion_theme.json`.
CHECK: dark navy page with a rounded sidebar panel on the left and the glowing header art top right.

## PHASE 2 — Load data (15 min)
1. Home > Get data > **Text/CSV**. Load each of these 6 (select all in one go if you prefer):
   fact_projects.csv, fact_generation.csv, fact_policy_levers.csv, fact_fx_sensitivity.csv, fact_capital_stack.csv, dim_risk.csv
2. Click **Transform Data** (not Load). In each table confirm column types:
   - fact_projects: scenario, project, state, status, cod_decade = Text; cod_year = Whole number; capacity_gw, capacity_factor, risk_score, bankability_score, min_dscr, *_irr_pct, risk_c1..c6, gen_2050_twh = Decimal; total_capex_inr_cr, overnight_capex_inr_cr, idc_inr_cr, prob_dscr_ok_pct = Whole number; dscr_ok = True/False.
   - fact_generation: year = Whole number; gen_twh = Decimal.
   - fact_policy_levers: projects_clearing_dscr, sort = Whole; gw_unlocked = Decimal.
   - fact_fx_sensitivity: avg_min_dscr = Decimal; sort = Whole. fact_capital_stack: share_pct = Decimal. dim_risk: sort Whole, weight Decimal.
3. **Close & Apply**.
CHECK: Data pane shows 6 tables. fact_projects has 30 rows (10 projects × 3 scenarios): Table view > fact_projects.

## PHASE 3 — Model (15 min)
1. Home > Modeling > **New table** > paste: `dim_state = DISTINCT ( fact_projects[state] )`. This is a TABLE with one column, `state`.
2. Model view (left icon). Drag **dim_state[state] → fact_projects[state]**: Cardinality One-to-many, Cross-filter direction **Single**, active.
3. Drag **dim_state[state] → fact_generation[state]**: same settings.
4. All other tables stay unconnected (that is correct).
5. Sort-by-column (Table view > select the column > Column tools > Sort by column):
   - dim_risk[dimension] by dim_risk[sort]
   - fact_policy_levers[lever] by fact_policy_levers[sort]
   - fact_fx_sensitivity[fx_case] by fact_fx_sensitivity[sort]
6. Summarisation: select **fact_projects[cod_year]** and **fact_generation[year]** > Column tools > Summarization = **Don't summarize**.
7. Hide clutter: right-click > Hide in report view on fact_projects[dscr_ok], overnight_capex_inr_cr, the sort columns, and dim_state is visible (needed for slicer).
CHECK: Model view shows dim_state in the middle with exactly two lines to fact_projects and fact_generation.

## PHASE 4 — Measures (30 min)
Open `fusion_all_measures.dax`. Create each measure with: **right-click table `fact_projects` > New measure** (this puts it in the right home table), paste ONE measure, press Enter. Do not paste the `dim_state` table line again.
Order: Selected Scenario > 9 core measures > 8 KPI text > Gen TWh > Risk Contribution > 4 colour helpers (23 measures total).
Then set formats (select measure > Measure tools): Investment L Cr = Decimal 2 · Capacity GW = Decimal 1 · Gen 2050 TWh = Whole · Avg Project IRR, Avg Equity IRR = Decimal 2 · Avg Risk = Decimal 1 · Gen TWh = Decimal 1.
If any measure landed in the wrong table: select it > Measure tools > Home table = fact_projects.
CHECK (build a throwaway Card visual for each, Scenario = Base): Investment L Cr = **5.28** · Gen 2050 TWh = **62** · Avg Project IRR = **7.21** · Avg Risk = **53.1** · DSCR OK Count = **6** · Bankable Count = **3** · Project Count = **10**. If any differs, stop and fix before building visuals. Delete the throwaway cards.

## PHASE 5 — Slicers and header (20 min)
Set position for every item here via **Format visual > General > Properties > Advanced options** (X, Y, Width, Height).
**5.1 Scenario slicer** — Slicer visual, field `fact_projects[scenario]`. Format: Slicer settings > Style = **Dropdown**; Selection > **Single select ON**, **Select all OFF**. X192 Y159 W200 H38. Click "Base" in it. Title off; border colour #1F3A5A, background #0E1F33.
**5.2 State slicer** — Slicer, field **`dim_state[state]`** (NOT fact_projects). Dropdown, Single select OFF, Select all ON. X402 Y159 W200 H38.
**5.3 Info text** — Insert > Text box: `DSCR covenant 1.30x · gearing 65% · 18-yr tenor · Monte Carlo 5,000 draws/project` — 11pt, #8FA6C1, X612 Y165 W900 H26.
**5.4 Header text boxes** (transparent background, no border, placed over the art):
 - Kicker: `FINANCIAL READINESS · INVESTMENT RISK` — 11pt bold #F5A623, X218 Y24 W500 H16
 - Title: `Financing India's Fusion Future` — Georgia 42 bold, white, X218 Y38 W900 H52
 - Subtitle: `A Financial Readiness & Investment Risk Assessment for Commercial Nuclear Fusion (2026–2050)` — 14pt #CFE6F7, X218 Y94 W1000 H22
 - Top-right: `ILLUSTRATIVE PROJECT PIPELINE` (11 bold #F5A623) + two lines `Constant-2026 ₹ crore · USD/INR 95.5` and `Real NPCIL sites · plants modelled, not announced` (11pt, white), right-aligned, X1500 Y20 W390 H60
 - 4 chips: Insert > Shapes > Rectangle, Rounded corners 99, fill white 92% transparent, border white 80% transparent, text 11pt: `⚡ Clean Energy`, `📈 Stronger Economy`, `🇮🇳 Brighter India`, `🏛 SHANTI Act 2025 · 100 GW nuclear by 2047`. Y118 H22; X218 (W110), X338 (W130), X478 (W120), X608 (W290).
**5.5 Sidebar** — text at top: `FUSION FINANCE` (Georgia 17 bold white, X22 Y22 W150) and `INDIA · 2026–2050` (10pt #F5A623, X22 Y66). 8 buttons (Insert > Buttons > Blank): X20 W150 H34, Y = 104, 144, 184, 224, 264, 304, 344, 384. Text: Overview, Investment Analysis, Risk Assessment, Scenario Analysis, State & Capacity, Financial Metrics, Banking & Lending, Data Explorer. Overview fill #1D8A5F, white text; the rest transparent, text #8FA6C1. Quote text box X20 Y1000 W150 H40: `From Possibility to Progress` (Georgia italic 12, #8FA6C1).
CHECK: choosing Scenario = Base in slicer still leaves the page blank of charts (none built yet) and nothing errors.

## PHASE 6 — KPI cards (20 min)
Visual type: **Card (new)** (or classic Card). Six cards, all Y206 W278 H100, X = 192, 480, 768, 1056, 1344, 1632.
For each: field = the KPI measure below; **Visual > Callout value** font Segoe UI Semibold 30 and the colour shown; **General > Title** on, text and 12pt #8FA6C1; **Subtitle** on, 11pt #8FA6C1 (static text, or for 1 and 3: fx > Field value > the KPI Sub measure); **Effects > Background** #0E1F33; **Visual border** on, colour = card colour, width 1.5, radius 14.

| # | X | Field | Title | Subtitle | Colour |
|---|---|---|---|---|---|
| 1 | 192 | KPI Investment | Total Investment Required | KPI Sub 1 (fx) | #4A9EFF |
| 2 | 480 | KPI Generation | Annual Generation, 2050 | plants operating by 2050 | #2EC27E |
| 3 | 768 | KPI IRR | Average Project IRR | KPI Sub 3 (fx) | #A78BFA |
| 4 | 1056 | KPI Risk | Average Risk Score | weighted, 6 dimensions | #F25C5C |
| 5 | 1344 | KPI DSCR | DSCR ≥ 1.30x | min DSCR, ramp-up year | #22D3EE |
| 6 | 1632 | KPI Bankable | Fully Bankable | DSCR ok AND P(clear) ≥ 70% | #F5A623 |

CHECK (Base): ₹5.28 L Cr · 62 TWh · 7.21% · 53.1 / 100 · 6 of 10 · 3 of 10. Switch slicer to Conservative: ₹6.34 L Cr · 33 TWh · 4.42% · 53.1 · 0 of 10 · 0 of 10. Accelerated: ₹4.49 L Cr · 65 TWh · 9.37% · 53.1 · 9 of 10 · 8 of 10. Return slicer to Base.

## PHASE 7 — Row 1 charts, Y315 (30 min)
Common for ALL chart visuals from here on: Title on (14pt Segoe UI Semibold #E8F0FA, left), Subtitle on (10.5pt #8FA6C1), Background #0E1F33, Visual border #1F3A5A radius 14, grid lines #1B3350, axis text 10pt #8FA6C1, Legend off unless stated.

**7.1 Project Risk vs Bankability** — Scatter chart. X192 Y315 W708 H214.
 Fields: Values = `project`; X Axis = `risk_score` (aggregation **Average**); Y Axis = `bankability_score` (**Average**); Size = `capacity_gw` (**Sum**); Legend = `cod_decade`.
 Format: X axis min 48 max 58, title `Risk score (higher = riskier)`; Y axis min 40 max 85, title `Bankability`; Markers > Colours: 2044-2045 = #F25C5C, 2046-2048 = #F5A623, 2049+ = #2EC27E; Legend off. Title `Project Risk vs Bankability`, subtitle `Bubble = capacity (GW) · colour = commissioning decade`.
**7.2 Capacity by State (GW)** — Clustered bar chart. X910 Y315 W425 H214. Y axis = `dim_state[state]`... use `fact_projects[state]`; X axis = measure **Capacity GW**. Sort by Capacity GW descending. Bar colour #4A9EFF, data labels off, X axis 0–2. Expected: Rajasthan 2.0, Tamil Nadu 1.3, Gujarat 1.0, Uttar Pradesh 1.0, Maharashtra/Karnataka/Haryana/West Bengal 0.8.
**7.3 Capital Stack by Instrument** — Donut chart. X1344 Y315 W566 H214. Legend = `instrument`; Values = `share_pct` (Sum). Slice colours in order: #4A9EFF, #2EC27E, #F5A623, #F25C5C, #A78BFA, #22D3EE. Legend ON, position Right, 10pt. Inner radius ~60%. Detail labels off. Expected shares: Commercial bank debt 24.7, ECB 14.3, Green & transition bonds 13.0, Multilateral 13.0, Sponsor/PSU equity 24.5, Private equity & climate VC 10.5 (total 100).
CHECK: scatter shows 10 bubbles, a red cluster at 2044–2045 with Kalpakkam far lower-right, green for Haripur/Gorakhpur.

## PHASE 8 — Row 2 charts, Y538 (35 min)
**8.1 Project Portfolio Snapshot** — Table. X192 Y538 W849 H283.
 Columns in this order: project, state, cod_year, capacity_gw, total_capex_inr_cr, risk_score, bankability_score, project_irr_pct, min_dscr, prob_dscr_ok_pct, status. For numeric columns choose aggregation **Don't summarize** (click field dropdown). Rename headers: Project, State, COD, GW, ₹ Cr, Risk, Bank., IRR%, DSCR, P(≥1.3), Status.
 Number formats (Column tools): capacity_gw 0.0 · total_capex 0 with thousands separator · risk, bankability 0.0 · irr 0.00 · dscr 0.00 · prob 0"%" (custom format `0"%"`).
 Format: Style > None/Minimal; Values font 10pt white, row padding 2, grid horizontal #162C46, header 10pt #8FA6C1 bold, no vertical grid. Slicer Scenario already filters it.
 Conditional formatting (Format > Cell elements > select the column > **Font color** (or Background colour for status) > fx > Format style **Field value** > Based on field: the measure):
 - risk_score → Font colour → `Risk Color`
 - min_dscr → Font colour → `DSCR Color`
 - status → Font colour → `Status Color`
**8.2 Monte Carlo** — Clustered bar. X1051 Y538 W425 H283. Y axis = `project`; X axis = `prob_dscr_ok_pct` (aggregation **Maximum**). Sort by prob descending. Bars: Columns > Colours > fx > Format style **Field value** > `Prob Color`. X axis 0–100. Title `Monte Carlo: P(DSCR ≥ 1.30x)`, subtitle `5,000 correlated draws / project`. Make sure all 10 category labels show (turn off auto-skip: increase height only if needed, Y axis label font 9pt).
**8.3 Risk Contribution by Dimension** — Clustered bar. X1486 Y538 W425 H283. Y axis = `dim_risk[dimension]`; X axis = measure **Risk Contribution**. Colour #22D3EE. Expected (Base): Technology Maturity 18.8, Regulatory & Licensing 8.6, Fuel & Supply Chain 7.9, Construction & EPC 8.4, Offtake / Counterparty 6.3, Grid Evacuation 3.1 (sum = 53.1 = Avg Risk).
CHECK: table last two rows are Gorakhpur (DSCR 1.70, Bankable) and Haripur (1.80, Bankable). Kalpakkam row: DSCR 0.77 red, Not Bankable, P = 4%.

## PHASE 9 — Row 3 charts, Y830 (25 min)
**9.1 Projected Generation (TWh)** — Line chart. X192 Y830 W566 H209. X axis = `fact_generation[year]` (Categorical); Y axis = measure **Gen TWh**; Legend = `fact_generation[scenario]`. Line colours: Conservative #4A9EFF, Base #2EC27E, Accelerated #F5A623; markers on, smooth lines on; Legend on, top. This chart ignores the Scenario slicer on purpose (it compares scenarios) but obeys the State slicer. Expected 2050: Conservative 33 · Base 62 · Accelerated 65.
**9.2 FX Sensitivity** — Clustered column. X768 Y830 W566 H209. X axis = `fx_case`; Y axis = `avg_min_dscr` (Average). Y axis min **1.0**, max **1.5**. Columns > Colours > **Vary colours by category** ON: Spot #2EC27E, Mild +10% #F5A623, Severe +20% #F25C5C, Hedged #4A9EFF. Data labels on, 0.00. Title `FX Sensitivity — ECB tranche (22% of debt)`, subtitle `Portfolio avg min DSCR · covenant 1.30x`. Expected: 1.36 / 1.34 / 1.31 / 1.36 (read exact from data labels).
**9.3 Hypothetical Policy Levers** — Clustered bar. X1344 Y830 W566 H209. Y axis = `lever`; X axis = `projects_clearing_dscr` (Max), axis max **10**, colour #2EC27E, data labels on. Title `Hypothetical Policy Levers`, subtitle `Projects clearing DSCR ≥ 1.30x (of 10) · none currently exist for fusion`. Expected: 6, 9, 9, 9, 10.
**9.4 Footer** — Text box X192 Y1053 W1718 H12... use H20: Georgia italic 11, centred, #8FA6C1: `"Fusion is not just an energy source — it is a test of whether the financing can keep pace."`
CHECK: all 9 cards visible, no overlap, nothing overflows the 1080 height.

## PHASE 10 — Interactivity and polish (15 min)
1. View > **Selection pane**: name each visual (e.g. kpi_investment, scatter_risk) — keeps the file tidy.
2. Home > **Edit interactions**: click the Scenario slicer > for the **Generation line** choose the "None" icon (so it keeps showing all 3 scenarios). Click the State slicer and leave the rest as Filter.
3. Page > Format page > Page information > Name = `Overview`. Hide page tabs: Format page > Page background... (optional) or publish as a single page.
4. File > Options > Current file > Report settings: tick "Always open in Fit to page".
5. Test every combination: 3 scenarios × All states / Rajasthan / Tamil Nadu. Numbers must change; no "multiple values" errors.
FIX if cards go blank when a State is chosen with scenarios: the State slicer filters correctly because dim_state connects to fact_projects.

## PHASE 11 — Final QA checklist
□ Canvas 1920×1080 □ Base shows 5.28 / 62 / 7.21 / 53.1 / 6 of 10 / 3 of 10 □ Conservative and Accelerated match the table in BUILD_GUIDE.md □ Capital stack sums to 100 □ Gen line has 3 scenarios □ Monte Carlo has 10 bars □ "ILLUSTRATIVE" and "Hypothetical" labels visible □ No visual overlaps (Selection pane) □ File saved as `fusion_finance_dashboard.pbix`.

## PHASE 12 — Export and publish
- Screenshot: View > Full screen (Alt+Enter) on a 1920×1080 display, then Win+Shift+S. Or File > Export > PDF.
- Share: Home > Publish > My workspace; Service > File > Embed report > Publish to web (public) only if no sensitive data (yours is illustrative, so it is safe).
- GitHub: add the .pbix, the screenshot, model.py, data/, and assumptions_register.csv. README: first line = screenshot, then Findings, Method, Assumptions, Limitations.

## Findings to quote (Base scenario; all in constant-2026 ₹)
- 10 modelled plants, 8.5 GW, ₹5.28 L Cr incl. interest during construction (~28% of the ~₹19 L Cr estimated for the 100 GW national nuclear target).
- 6 of 10 clear a 1.30x DSCR covenant; only 3 are fully bankable (also ≥ 70% pass rate over 5,000 correlated simulations).
- First-of-a-kind Kalpakkam: DSCR 0.77x; last plant Haripur: 1.80x → cost learning is the main driver of bankability.
- Hypothetical support (VGF 30% + 6.5% concessional debt) lifts all 10 plants above 1.30x.
- Accelerated vs Conservative: investment ₹4.49 vs ₹6.34 L Cr; project IRR 9.37% vs 4.42%.
