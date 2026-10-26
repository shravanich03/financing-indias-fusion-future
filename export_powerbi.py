"""Turns data/dashboard.json (written by model.py) into the CSVs that Power BI loads (written to powerbi/)."""
import json, os, pandas as pd
os.makedirs("powerbi", exist_ok=True)
D = json.load(open("data/dashboard.json")); P = pd.DataFrame(D["P"])
for i in range(6): P[f"risk_c{i+1}"] = P.x.apply(lambda v: v[i])
P["cod_decade"] = P.y.apply(lambda y: "2044-2045" if y <= 2045 else "2046-2048" if y <= 2048 else "2049+")
P["gen_2050_twh"] = (P.gw * 8.76 * P.cf * (P.y <= 2050)).round(2)   # only plants operating by 2050
(P.drop(columns="x").rename(columns={"sc":"scenario","n":"project","s":"state","y":"cod_year","gw":"capacity_gw","cf":"capacity_factor",
  "cx":"total_capex_inr_cr","cxo":"overnight_capex_inr_cr","idc":"idc_inr_cr","r":"risk_score","b":"bankability_score","irr":"project_irr_pct",
  "eirr":"equity_irr_pct","d":"min_dscr","p":"prob_dscr_ok_pct","f":"status"}).to_csv("powerbi/fact_projects.csv", index=False))
pd.DataFrame([dict(scenario=r.sc, project=r.n, state=r.s, year=y, gen_twh=round(r.gw*8.76*r.cf, 2) if r.y <= y else 0)
              for r in P.itertuples() for y in range(2044, 2051)]).to_csv("powerbi/fact_generation.csv", index=False)
pd.DataFrame(D["L"]).rename(columns={"l":"lever","n":"projects_clearing_dscr","gw":"gw_unlocked"}).assign(sort=range(5)).to_csv("powerbi/fact_policy_levers.csv", index=False)
pd.DataFrame(D["X"]).rename(columns={"l":"fx_case","v":"avg_min_dscr"}).assign(sort=range(4)).to_csv("powerbi/fact_fx_sensitivity.csv", index=False)
pd.DataFrame(D["F"]).rename(columns={"l":"instrument","v":"share_pct"}).to_csv("powerbi/fact_capital_stack.csv", index=False)
pd.DataFrame({"dimension": D["DIM"], "sort": range(6), "weight": [.28,.17,.15,.15,.15,.10]}).to_csv("powerbi/dim_risk.csv", index=False)
print("Power BI files written to powerbi/")
