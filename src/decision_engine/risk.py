from __future__ import annotations
import numpy as np
import pandas as pd

def shrink_cov(returns:pd.DataFrame,annualization=12,shrink=.25):
    s=returns.cov()*annualization
    diag=pd.DataFrame(np.diag(np.diag(s)),index=s.index,columns=s.columns)
    return (1-shrink)*s+shrink*diag

def portfolio_vol(w,cov):
    x=np.asarray(w,float); C=np.asarray(cov,float)
    return float(np.sqrt(max(x@C@x,0)))

def drawdown(r:pd.Series):
    wealth=(1+r.fillna(0)).cumprod()
    return wealth/wealth.cummax()-1

def performance_stats(r:pd.Series,periods=12):
    r=r.dropna()
    wealth=(1+r).cumprod()
    ann=float(wealth.iloc[-1]**(periods/len(r))-1)
    vol=float(r.std()*np.sqrt(periods))
    dd=drawdown(r)
    return {
        "annual_return":ann,
        "annual_vol":vol,
        "sharpe":float(r.mean()*periods/(vol+1e-12)),
        "max_drawdown":float(dd.min()),
        "hit_rate":float((r>0).mean()),
    }
