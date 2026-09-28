import numpy as np
from decision_engine.data import synthetic_prices
from decision_engine.signals import monthly_signal_panel
from decision_engine.engine import run_engine
from decision_engine.execution import estimate_costs

def test_signal_timing_has_future_return_available():
    p=synthetic_prices(1000,seed=1)
    m,r,panel=monthly_signal_panel(p)
    assert panel["date"].max()<=m.index.max()
    assert panel["date"].min()>m.index.min()

def test_execution_costs_nonnegative():
    import pandas as pd
    d=pd.Series({"SPY":.10,"TLT":-.10})
    c=estimate_costs(d)
    assert (c.total_cost>=0).all()
    assert c.total_cost.sum()>0

def test_engine_accounting_and_constraints():
    p=synthetic_prices(1600,seed=2)
    out=run_engine(p,min_history=24)
    assert len(out["returns"])>20
    w=out["weights"].pivot(index="return_date",columns="asset",values="weight")
    assert np.allclose(w.sum(axis=1),1,atol=1e-5)
    assert (w.max(axis=1)<=.25001).all()
    d=out["decision_log"]
    assert np.allclose(d["gross_return"]-d["execution_cost"],d["net_return"],atol=1e-12)
    assert (d["ex_ante_vol"]<=.18001).all()

def test_attribution_sums_to_gross_return():
    p=synthetic_prices(1600,seed=3)
    out=run_engine(p,min_history=24)
    a=out["attribution"].groupby("date")["gross_return_contribution"].sum()
    d=out["decision_log"].set_index("return_date")["gross_return"]
    common=a.index.intersection(d.index)
    assert np.allclose(a.loc[common],d.loc[common],atol=1e-12)
