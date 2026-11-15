# Portfolio Decision Engine

A monthly ETF backtest that records why each trade happened and reconciles the resulting P&L back to asset contributions and estimated execution costs.

## Results

**The strategy improved Sharpe and reduced drawdown, but gave up its small gross return advantage after costs.** The historical market-data run used adjusted Yahoo Finance prices for SPY, QQQ, IWM, EFA, EEM, IEF, TLT, GLD, DBC and VNQ. Prices span January 2012–October 2026. The walk-forward evaluation spans **February 2014–October 2026** (153 months).

| Portfolio | CAGR | Annualized volatility | Sharpe (zero risk-free rate) | Max drawdown |
| --- | ---: | ---: | ---: | ---: |
| Decision Engine, gross | 8.23% | 8.75% | 0.95 | -16.56% |
| Decision Engine, net | 8.12% | 8.75% | 0.94 | -16.61% |
| Equal weight, before costs | 8.21% | 10.47% | 0.81 | -21.05% |

Average two-way target turnover was **20.98% per month**. Modeled spread and impact lowered strategy CAGR by **10.94 basis points per year**. The equal-weight comparator is a frictionless monthly target-weight benchmark, and the code does not estimate its turnover or charge it trading costs. Strategy turnover measures changes in month-end target weights, not changes from drifted pre-trade holdings.

### From signal to P&L

The score combines 12–1 momentum, six-month trend and inverse-volatility ranks standardized across the ETF universe. The optimizer produces long-only target weights subject to concentration, volatility and turnover limits. Each month's signal is applied to the next month's return, and the trade log keeps estimated costs separate from gross asset contributions. CI checks signal timing and attribution reconciliation.

```bash
pip install -r requirements.txt
PYTHONPATH=src python scripts/run_engine.py --mode live
```

The dated snapshot uses completed months through October 2026. The live command fetches updated data, so its end date and figures may differ. To test the pipeline without a data download, use `--mode synthetic`.
