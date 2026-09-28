from __future__ import annotations
import numpy as np
import pandas as pd

def _cross_sectional_z(x:pd.Series)->pd.Series:
    sd=x.std()
    if not np.isfinite(sd) or sd<1e-12:
        return pd.Series(0.0,index=x.index)
    return (x-x.mean())/sd

def monthly_signal_panel(prices:pd.DataFrame):
    m=prices.resample("ME").last()
    r=m.pct_change(fill_method=None)
    # Every signal at month t uses data ending at t; backtest applies it to t+1 return.
    mom_12_1=m.shift(1)/m.shift(12)-1
    trend_6=m/m.shift(6)-1
    vol_3=r.rolling(3).std()*np.sqrt(12)

    rows=[]
    for d in m.index:
        if d not in mom_12_1.index: continue
        mom=_cross_sectional_z(mom_12_1.loc[d])
        trend=_cross_sectional_z(trend_6.loc[d])
        defensive=_cross_sectional_z(-vol_3.loc[d])
        composite=.50*mom+.30*trend+.20*defensive
        for a in m.columns:
            rows.append({
                "date":d,"asset":a,
                "momentum":mom.get(a,np.nan),
                "trend":trend.get(a,np.nan),
                "defensive":defensive.get(a,np.nan),
                "composite":composite.get(a,np.nan),
            })
    panel=pd.DataFrame(rows)
    return m,r,panel.dropna()

def signal_vector(panel:pd.DataFrame,date,assets):
    x=panel.loc[panel.date==date].set_index("asset")["composite"]
    return x.reindex(assets)
