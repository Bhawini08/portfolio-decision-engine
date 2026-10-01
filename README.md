# Portfolio Decision Engine

An end-to-end systematic investment research engine connecting signal formation, portfolio construction, execution assumptions, risk controls, realized performance, and attribution.

The project is designed around one institutional question:

> A signal changed. Should the portfolio trade, by how much, at what expected cost, and what ultimately drove the resulting P&L?

## Pipeline

1. Raw market data
2. Lagged signal formation
3. Cross-sectional signal normalization
4. Expected-return mapping
5. Covariance estimation
6. Constrained portfolio optimization
7. Turnover and execution-cost model
8. Risk-control audit
9. Rebalance decision log
10. Realized P&L and attribution

## Default signals

- 12-1 cross-sectional momentum
- 6-month trend
- inverse-volatility defensive signal

Signals are formed exclusively from information available before the return they are evaluated against.

## Portfolio controls

- long-only
- full investment
- maximum asset weight
- portfolio volatility ceiling
- turnover ceiling
- turnover penalty in the optimization objective
- explicit transaction-cost drag

## Execution assumptions

The execution layer separates:

- linear spread/slippage cost
- nonlinear impact cost

The assumptions are intentionally stylized and transparent. This is not an order-book simulator.

## Outputs

- strategy and benchmark returns
- portfolio weights
- signal history
- trade blotter
- expected execution costs
- asset-level return contribution
- turnover
- risk diagnostics
- drawdowns
- decision log at every rebalance

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

pytest -q
python scripts/run_engine.py --mode synthetic
python scripts/run_engine.py --mode live

streamlit run dashboard/app.py
```

Synthetic mode provides deterministic CI. Live mode uses liquid ETF proxies for empirical validation.

## What the repository produces

Each rebalance creates an auditable chain from signal date to next-period return: signal ranks, expected returns, optimized weights, trades, estimated implementation cost, ex-ante volatility, realized gross and net return, and asset-level attribution. Generated outputs are written to `results/` and are intentionally reproducible rather than committed as static current-market results.

## Validation

Tests enforce signal timing, portfolio constraints, gross-to-net accounting, non-negative execution costs, and attribution reconciliation. GitHub Actions runs the full test suite and deterministic synthetic engine on every push and pull request.

## Limitations

Signals, expected-return mapping, and execution costs are stylized research assumptions. ETF closing prices do not reproduce institutional execution, and the engine should not be interpreted as evidence of deployable alpha without broader out-of-sample and implementation validation.

