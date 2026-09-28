from __future__ import annotations
import numpy as np
import pandas as pd
from .signals import monthly_signal_panel,signal_vector
from .risk import shrink_cov,performance_stats
from .portfolio import expected_returns_from_signal,optimize_portfolio
from .execution import estimate_costs

def run_engine(prices,min_history=24,max_weight=.25,vol_limit=.18,turnover_limit=.60):
    monthly,returns,panel=monthly_signal_panel(prices)
    assets=list(monthly.columns)
    prev=pd.Series(1/len(assets),index=assets)

    strategy=[]; benchmark=[]; dates=[]
    weights=[]; signals=[]; blotter=[]; attribution=[]; decisions=[]

    signal_dates=sorted(panel["date"].unique())
    for signal_date in signal_dates:
        i=monthly.index.get_loc(signal_date)
        if i<min_history or i+1>=len(monthly.index): continue

        next_date=monthly.index[i+1]
        hist=returns.loc[:signal_date].dropna()
        if len(hist)<min_history: continue
        sig=signal_vector(panel,signal_date,assets)
        if sig.isna().any(): continue

        mu=expected_returns_from_signal(sig)
        cov=shrink_cov(hist.tail(60))
        w=optimize_portfolio(mu,cov,prev,max_weight,vol_limit,turnover_limit)

        delta=w-prev
        costs=estimate_costs(delta)
        cost=float(costs.total_cost.sum())
        next_r=returns.loc[next_date]
        gross=float(w@next_r)
        net=gross-cost
        bench_w=pd.Series(1/len(assets),index=assets)
        bench=float(bench_w@next_r)

        dates.append(next_date); strategy.append(net); benchmark.append(bench)
        for a in assets:
            weights.append({"signal_date":signal_date,"return_date":next_date,"asset":a,"weight":float(w[a])})
            signals.append({"signal_date":signal_date,"asset":a,"signal":float(sig[a]),"expected_return":float(mu[a])})
            attribution.append({"date":next_date,"asset":a,"weight":float(w[a]),"asset_return":float(next_r[a]),
                                "gross_return_contribution":float(w[a]*next_r[a])})
        for _,row in costs.iterrows():
            blotter.append({"signal_date":signal_date,"return_date":next_date,**row.to_dict()})
        decisions.append({
            "signal_date":signal_date,"return_date":next_date,
            "gross_return":gross,"execution_cost":cost,"net_return":net,
            "turnover":float(delta.abs().sum()),
            "ex_ante_vol":float(np.sqrt(w.to_numpy()@cov.to_numpy()@w.to_numpy())),
            "top_signal_asset":str(sig.idxmax()),"top_weight_asset":str(w.idxmax()),
        })
        prev=w

    perf=pd.DataFrame({"strategy":strategy,"equal_weight":benchmark},index=dates)
    summary=pd.DataFrame([
        {"portfolio":"decision_engine",**performance_stats(perf["strategy"])},
        {"portfolio":"equal_weight",**performance_stats(perf["equal_weight"])},
    ])
    return {
        "returns":perf,
        "summary":summary,
        "weights":pd.DataFrame(weights),
        "signals":pd.DataFrame(signals),
        "blotter":pd.DataFrame(blotter),
        "attribution":pd.DataFrame(attribution),
        "decision_log":pd.DataFrame(decisions),
    }
