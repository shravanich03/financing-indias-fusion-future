"""Fusion financing model v4 - constant-2026 INR, real debt rate, IDC included, correlated Monte Carlo.
Run: python model.py  -> writes data/*.csv + data/dashboard.json  (every input is listed in assumptions_register.csv)"""
import numpy as np, pandas as pd, json
import os; os.makedirs("data",exist_ok=True)
rng=np.random.default_rng(42); O='data/'
FX=95.5; INFL=.045; NOM=.09; RD=(1+NOM)/(1+INFL)-1          # real cost of debt ~4.3%
TAX=.2517; TENOR=18; GEAR=.65; OPEX=.025; LIFE=30; THR=1.30; ECB=.22
CAPEX0=8500; LR=.12; TAR=11.5                                # $/kW first plant, learning rate / doubling, Rs/kWh real
SC={'Conservative':(1.20,.90,-.05,3),'Base':(1,1,0,0),'Accelerated':(.85,1.05,.03,-2)}
W=np.array([.28,.17,.15,.15,.15,.10]); DIM=['Technology Maturity','Regulatory & Licensing','Fuel & Supply Chain','Construction & EPC','Offtake / Counterparty','Grid Evacuation']
OFF=dict(zip(['West Bengal','Haryana','Rajasthan','Uttar Pradesh','Karnataka','Tamil Nadu','Maharashtra','Gujarat'],[55,40,42,58,38,36,44,32]))
GRD=dict(zip(OFF,[40,35,28,42,30,26,30,24]))
PR=[('Kalpakkam Fusion Demo','Tamil Nadu',.5,2044,8),('Kudankulam Fusion Annexe','Tamil Nadu',.8,2045,7),('Tarapur Fusion Hub','Maharashtra',.8,2045,7),
('Kakrapar Fusion Park','Gujarat',1,2046,7),('Kaiga Fusion Station','Karnataka',.8,2046,7),('Rawatbhata Fusion','Rajasthan',1,2047,6),
('Narora Fusion Complex','Uttar Pradesh',1,2048,6),('Mahi Banswara Fusion','Rajasthan',1,2048,6),('Gorakhpur Fusion','Haryana',.8,2049,6),('Haripur Fusion','West Bengal',.8,2050,6)]
def dscr(gw,cx,cf,constr,rd=RD,v=0,cm=1,tm=1,fm=1,dl=0,fx=1):
    cap=cx*cm; idc=cap*(1-v)*GEAR*rd*(constr+dl)/2; debt=GEAR*cap*(1-v)+idc
    ds=debt*rd/(1-(1+rd)**-TENOR)*(1-ECB+ECB*fx)
    rev=gw*8760*1e6*np.minimum(cf*fm,.95)*.8*TAR*tm/1e7; eb=rev-OPEX*cap; tax=TAX*np.maximum(0,eb-(cap+idc)/25)
    return (eb-tax)/ds, idc
def irr(c):
    lo,hi=-.9,1.
    for _ in range(80):
        m=(lo+hi)/2
        if sum(x/(1+m)**t for t,x in enumerate(c))>0: lo=m
        else: hi=m
    return m*100
rows=[];mc=[]
base=[]; cum=0
for i,(n,s,gw,cod,cn) in enumerate(PR):
    cum+=gw; site=rng.uniform(.95,1.08)
    kw=CAPEX0*(cum/PR[0][2])**np.log2(1-LR)*site          # learning by doubling of cumulative GW
    r=np.array([78-2.2*i+rng.normal(0,2),48+rng.normal(0,4),58-1.2*i,62-1.5*i+rng.normal(0,3),OFF[s],GRD[s]]).clip(5,95)
    base.append((n,s,gw,cod,cn,kw*gw*1e6*FX/1e7,r,.78+.012*i))
for sc,(cm,tm,dcf,dly) in SC.items():
  for n,s,gw,cod,cn,cx,r,cf in base:
    cx2=cx*cm; cf2=cf+dcf; d,idc=dscr(gw,cx,cf2,cn,cm=cm,tm=tm); tot=cx2+idc
    ann=lambda x:x
    rev=lambda t:gw*8760*1e6*min(cf2,.95)*(.8 if t==1 else .9 if t==2 else 1)*TAR*tm/1e7
    dep=tot/25; ds=(GEAR*cx2+idc)*RD/(1-(1+RD)**-TENOR)
    pc=[-cx2/cn]*cn+[]; ec=[-(1-GEAR)*cx2/cn]*cn
    for t in range(1,LIFE+1):
        eb=rev(t)-OPEX*cx2; tx=TAX*max(0,eb-dep); pc.append(eb-tx); ec.append(eb-tx-(ds if t<=TENOR else 0))
    z=rng.normal(size=(5000,2)); com=rng.normal(size=5000)[:,None]; zi=np.sqrt(.5)*com+np.sqrt(.5)*z
    dd,_=dscr(gw,cx,cf2,cn,cm=cm*np.exp(.2*zi[:,0]-.02),tm=tm*np.exp(-.3*.1*com[:,0]+.1*z[:,1]*.95),fm=rng.normal(1,.07,5000),dl=np.clip(np.round(1.5+1.5*zi[:,0]),0,6))
    p=(dd>=THR).mean()*100; rk=float((r*W).sum()); bs=float(np.clip(100*(.5*min(d/1.6,1)+.5*(1-rk/100)),0,100))
    f='Bankable' if d>=THR and p>=70 else 'Marginal' if d>=1.15 or p>=40 else 'Not Bankable'
    rows.append(dict(sc=sc,n=n,s=s,y=cod+dly,gw=gw,cf=round(cf2,3),cx=round(tot),cxo=round(cx2),idc=round(idc),r=round(rk,1),b=round(bs,1),irr=round(irr(pc),2),eirr=round(irr(ec),2),d=round(float(d),2),p=round(p),f=f,dscr_ok=bool(d>=THR),x=[round(float(a),2) for a in r*W]))
P=pd.DataFrame(rows); P.to_csv(O+'fact_projects.csv',index=False)
B=[(n,s,gw,cn,cx,cf) for n,s,gw,cod,cn,cx,r,cf in base]
def lever(v=0,nom=NOM):
    rd=(1+nom)/(1+INFL)-1; ok=[(g,dscr(g,cx,cf,cn,rd=rd,v=v)[0]>=THR) for n,s,g,cn,cx,cf in B]
    return sum(o for _,o in ok),round(sum(g for g,o in ok if o),1)
L=[dict(l=l,n=lever(v,nom)[0],gw=lever(v,nom)[1]) for l,v,nom in [('No support (base)',0,NOM),('VGF 20% of capex',.2,NOM),('VGF 30% of capex',.3,NOM),('Concessional debt 6.5%',0,.065),('VGF 30% + 6.5% debt',.3,.065)]]
X=[dict(l=l,v=round(float(np.mean([dscr(g,cx,cf,cn,fx=f)[0]/h for n,s,g,cn,cx,cf in B])),2)) for l,f,h in [('Spot',1,1),('Mild +10%',1.1,1),('Severe +20%',1.2,1),('Hedged (3% cost)',1,1+ECB*.03)]]
T=P[P.sc=='Base'];tc=T.cx.sum();dsh=GEAR
F=[dict(l=l,v=round(v*100,1)) for l,v in [('Commercial bank debt (INR)',.65*.38),('ECB / foreign-currency loan',.65*.22),('Green & transition bonds',.65*.20),('Multilateral (ADB/WB/NDB)',.65*.20),('Sponsor / PSU equity',.35*.70),('Private equity & climate VC',.35*.30)]]
json.dump(dict(P=rows,L=L,X=X,F=F,DIM=DIM),open(O+'dashboard.json','w'),default=lambda o:o.item() if hasattr(o,'item') else str(o))
pd.DataFrame(L).to_csv(O+'fact_policy_levers.csv',index=False);pd.DataFrame(X).to_csv(O+'fact_fx_sensitivity.csv',index=False);pd.DataFrame(F).to_csv(O+'fact_capital_stack.csv',index=False)
# integrity checks
assert abs(sum(f['v'] for f in F)-100)<.2; assert (P.cx>=P.cxo).all()
print('checks passed')
