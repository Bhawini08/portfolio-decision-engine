from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from .risk import portfolio_vol

def expected_returns_from_signal(signal:pd.Series,scale=.06):
    # Cross-sectional signal maps to a modest annual expected-return spread.
    x=signal.fillna(0)
    mx=max(float(x.abs().max()),1.0)
    return scale*x/mx

def optimize_portfolio(mu,cov,prev,max_weight=.25,vol_limit=.18,turnover_limit=.60,risk_aversion=4.0,turnover_penalty=.003):
    assets=list(mu.index); m=mu.to_numpy(float); C=cov.loc[assets,assets].to_numpy(float)
    p=prev.reindex(assets).fillna(0).to_numpy(float)
    if abs(p.sum()-1)>1e-8: p=np.repeat(1/len(assets),len(assets))

    def obj(w):
        utility=-(w@m-risk_aversion*(w@C@w))
        smooth_turnover=turnover_penalty*np.sum(np.sqrt((w-p)**2+1e-10))
        return float(utility+smooth_turnover)

    cons=[
        {"type":"eq","fun":lambda w:w.sum()-1},
        {"type":"ineq","fun":lambda w:turnover_limit-np.abs(w-p).sum()},
        {"type":"ineq","fun":lambda w:vol_limit**2-w@C@w},
    ]
    res=minimize(obj,p,method="SLSQP",bounds=[(0,max_weight)]*len(assets),
                 constraints=cons,options={"maxiter":3000,"ftol":1e-10})
    if not res.success:
        # Relax only the turnover cap on retry, never the risk or position limits.
        cons2=[cons[0],cons[2]]
        res=minimize(obj,p,method="SLSQP",bounds=[(0,max_weight)]*len(assets),
                     constraints=cons2,options={"maxiter":3000,"ftol":1e-10})
    if not res.success: raise RuntimeError("optimization failed: "+res.message)
    w=pd.Series(res.x,index=assets)
    if abs(w.sum()-1)>1e-5 or (w< -1e-7).any() or (w>max_weight+1e-6).any():
        raise RuntimeError("post-solve weight audit failed")
    if portfolio_vol(w,cov)>vol_limit+1e-5:
        raise RuntimeError("post-solve volatility audit failed")
    return w
