from __future__ import annotations
import numpy as np
import pandas as pd

DEFAULT_SPREAD_BPS={
    "SPY":1.0,"QQQ":1.0,"IWM":1.5,"EFA":2.0,"EEM":2.5,
    "IEF":1.0,"TLT":1.5,"GLD":1.5,"DBC":3.0,"VNQ":2.0,
}

def estimate_costs(delta:pd.Series,spread_bps=None,impact_bps=8.0):
    spread_bps=spread_bps or DEFAULT_SPREAD_BPS
    rows=[]
    for asset,trade in delta.items():
        q=abs(float(trade))
        spread=q*float(spread_bps.get(asset,2.0))/10000
        impact=(q**1.5)*impact_bps/10000
        rows.append({"asset":asset,"trade_weight":float(trade),"abs_trade_weight":q,
                     "spread_cost":spread,"impact_cost":impact,"total_cost":spread+impact})
    return pd.DataFrame(rows)

def total_cost(delta:pd.Series,spread_bps=None,impact_bps=8.0):
    return float(estimate_costs(delta,spread_bps,impact_bps)["total_cost"].sum())
