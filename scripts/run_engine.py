import argparse,json
from pathlib import Path
from decision_engine.data import synthetic_prices,live_prices
from decision_engine.engine import run_engine

p=argparse.ArgumentParser(); p.add_argument("--mode",choices=["synthetic","live"],default="synthetic"); args=p.parse_args()
prices=synthetic_prices() if args.mode=="synthetic" else live_prices()
res=run_engine(prices)

out=Path("results"); out.mkdir(exist_ok=True)
for name in ["returns","summary","weights","signals","blotter","attribution","decision_log"]:
    obj=res[name]
    obj.to_csv(out/f"{args.mode}_{name}.csv",index=(name=="returns"))

d=res["decision_log"]
metrics={
    "mode":args.mode,
    "rebalance_count":int(len(d)),
    "average_turnover":float(d.turnover.mean()),
    "total_execution_cost":float(d.execution_cost.sum()),
    "average_ex_ante_vol":float(d.ex_ante_vol.mean()),
}
(out/f"{args.mode}_metrics.json").write_text(json.dumps(metrics,indent=2))
print(res["summary"].to_json(orient="records",indent=2))
print(json.dumps(metrics,indent=2))
