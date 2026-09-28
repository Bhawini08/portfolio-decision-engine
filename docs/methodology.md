# Methodology

## Signal timing

Signals are calculated at month-end t from price history available through t.

The allocation generated from those signals is evaluated only on month t+1 returns. This one-period separation prevents the portfolio from earning the return used to create its own signal.

## Signals

### 12-1 momentum

Return from month t-12 to t-1, excluding the most recent month.

### Six-month trend

Six-month total return through signal formation.

### Defensive signal

Negative three-month realized volatility, favoring relatively lower-volatility assets.

Each signal is standardized cross-sectionally and combined into a transparent composite.

## Expected-return mapping

The composite signal is mapped to a modest annual expected-return spread. The mapping is deliberately conservative because raw signal z-scores are rankings, not literal return forecasts.

## Risk model

Monthly covariance is estimated from trailing history and shrunk toward its diagonal for numerical stability.

## Portfolio optimization

The portfolio maximizes expected return minus quadratic risk and turnover penalties subject to:

- full investment
- long-only weights
- maximum position size
- portfolio volatility ceiling
- turnover ceiling

If the turnover ceiling creates a numerical failure, the engine may retry without that ceiling but never relaxes position or volatility constraints. The decision log records realized turnover so this fallback remains visible.

## Execution model

Estimated implementation cost is the sum of:

- spread/slippage proportional to absolute trade size
- nonlinear impact proportional to trade size raised to 1.5

Costs are deducted from portfolio return at every rebalance.

## Attribution

Asset-level gross return contribution is weight times subsequent asset return. These contributions reconcile exactly to gross portfolio return. Execution costs are reported separately so gross alpha and implementation drag are not conflated.

## Decision log

Every rebalance records:

- signal date
- return date
- top-ranked signal
- largest resulting position
- turnover
- ex-ante volatility
- gross return
- execution cost
- net return

The log makes the research-to-P&L chain auditable.

## Limitations

Signals and execution costs are stylized. ETF closing prices do not reproduce institutional execution. The engine is intended to demonstrate research architecture, portfolio decision logic, and accounting discipline rather than claim deployable alpha without further validation.
