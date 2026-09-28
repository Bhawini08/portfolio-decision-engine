from __future__ import annotations
import numpy as np
import pandas as pd

ASSETS=["SPY","QQQ","IWM","EFA","EEM","IEF","TLT","GLD","DBC","VNQ"]

def synthetic_prices(n_days=2200,seed=19):
    rng=np.random.default_rng(seed)
    idx=pd.bdate_range("2017-01-03",periods=n_days)
    n=len(ASSETS)
    # Persistent latent factor creates realistic momentum/trend structure.
    factor=np.zeros(n_days)
    for t in range(1,n_days):
        factor[t]=0.96*factor[t-1]+rng.normal(0,.0018)
    beta=np.array([1.0,1.15,1.1,.9,1.05,-.25,-.40,.10,.35,.75])
    vols=np.array([.010,.013,.014,.011,.014,.004,.007,.008,.011,.012])
    drift=np.array([.00030,.00034,.00028,.00024,.00026,.00010,.00011,.00012,.00015,.00023])
    eps=rng.normal(0,vols,size=(n_days,n))
    ret=drift+factor[:,None]*beta+eps
    prices=100*np.exp(np.cumsum(np.log1p(np.clip(ret,-.95,None)),axis=0))
    return pd.DataFrame(prices,index=idx,columns=ASSETS)

def live_prices(start="2012-01-01",end=None):
    import yfinance as yf
    raw=yf.download(ASSETS,start=start,end=end,auto_adjust=True,progress=False,threads=False)
    if raw.empty: raise RuntimeError("Yahoo Finance returned no data")
    px=raw["Close"] if isinstance(raw.columns,pd.MultiIndex) else raw[["Close"]]
    px.columns=[str(c).upper() for c in px.columns]
    return px.dropna(how="any")
