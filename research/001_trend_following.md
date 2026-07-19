# Experiment 001: Simple Trend Following

## Status

Planned

## Research Question

Does a simple moving-average trend-following strategy produce better risk-adjusted performance than buy-and-hold after accounting for transaction costs and avoiding lookahead bias?

## Motivation

Trend following is one of the simplest systematic trading ideas: hold an asset when its recent price trend is positive and move out of the position when the trend is negative. 

This experiment is not intended to discover a production-ready trading strategy. Its purpose is to establish a reproducible baseline, validate the backtesting infrastructure, and study how implementation choices affect reported performance.

## Hypothesis

A moving-average crossover strategy may reduce large drawdowns compared with buy-and-hold, but it may also underperform during sideways markets because of repeated position changes. 

The strategy will be considered promising only if any improvement remains after transaction costs and is reasonably stable across assets, time periods, and parameter choices. 

## Strategy Definition

The initial strategy uses two simple moving averages:

- Fast moving average: 50 trading days
- Slow moving average: 200 trading days

The desired position is:

- Long with weight $1.0$ when the 50-day moving average is above the 200-day moving average
- In cash with weight $0.0$ otherwise

A signal calculated using prices available at the close of day `t` may only affect the portfolio beginning on day `t + 1`.

Short-selling and leverage are excluded from the initial experiment.

## Baseline

The primary baseline is buy-and-hold in the same asset over the same evaluation period.

A cash-only portfolio may also be included as a sanity-check baseline.

## Dataset

The initial asset universe is:

- SPY
- QQQ
- IWM
- EFA
- EEM
- TLT
- GLD

The experiment will use daily adjusted closing prices.

The exact data source, download rate, available date range, missing-value policy, and adjustment methodology will be recorded when the data pipeline is implemented. 

Assets will initially be evaluated independently rather than combined into one portfolio.

## Trading Assumptions

- Signals are generated using end-of-day data
- Trades occur no earlier than the following trading day
- No leverage
- No short-selling
- Uninvested capital earns zero interest in the first version
- Transaction costs are charged when the target position changes
- Taxes and market impact are excluded 

The first cost model will use a fixed cost in basis points applied to traded notional. Results will be reported under multiple cost assumptions rather than one supposedly exact value.

## Evaluation Metrics

The following metrics will be reported:

- Cumulative return
- Compound annual growth rate
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Maximum drawdown
- Calmar ratio
- Average turnover
- Number of position changes
- Percentage of time invested

The strategy will also be compared with buy-and-hold using:

- Equity curves
- Drawdown curves
- Calendar-year returns
- Rolling returns
- Rolling volatility
- Rolling Sharpe ratio

## Experimental Procedure

1. Load and validate adjusted daily prices.
2. Compute the 50-day and 200-day moving averages.
3. Generate the desired position using information available through day `t`.
4. Shift the position so returns begin no earlier than day `t + 1`.
5. Compute gross strategy returns.
6. Deduct transaction costs when the position changes.
7. Compute the same metrics for buy-and-hold.
8. Repeat the experiment for each asset.
9. Test nearby moving-average parameters.
10. Compare results across subperiods.

## Robustness Checks

The initial robustness analysis will include: 

- Multiple assets
- Multiple transaction-cost assumptions
- Nearby parameter combinations
- Earlier and later sample periods
- Performance before and after major market regimes
- Verification that conclusions are not driven by one asset or one period

Parameter combinations should be chosen before inspecting their results when practical.

## Threads to Validity

### Lookahead Bias

A backtest may accidentally use a signal and the same day's return. Signals must be shifted so that decisions use only information that was available at the time.

### Data Quality

Adjusted prices may differ across vendors. Missing dates, duplicate rows, invalid values, and corporate-action adjustments must be checked explicitly.

### Parameter Overfitting

Choosing the best moving-average windows after reviewing many alternatives can make an ordinary result appear significant.

### Survivorship and Selection Bias

The initial ETF universe consists of assets known today and was selected manually. Results therefore should not be treated as evidence that the strategy would have worked across all historically available investments.

### Transaction-Cost Modeling

A fixed basis-point cost is only an approximation. It does not fully represent bid-ask spreads, market impact, delayed execution, or changes in liquidity.

### Regime Dependence

Trend-following performance may depend heavily on a small number of extended market trends and may deteriorate during sideways periods.

### Statistical Uncertainty

A strong historical Sharpe ratio does not guarantee that the underlying expected return is positive. The number of independent market regimes may be much smaller than the number of daily observations.

## Success Criteria

This experiment is not successful merely because one backtest has a higher return than buy-and-hold.

The result will be considered worthy of further investigation if:

1. The implementation passes tests designed to detect lookahead and accounting errors.
2. The strategy reduces drawdown or improves risk-adjusted performance on more than one asset.
3. The result remains directionally similar under reasonable transaction costs.
4. Nearby parameter choices produce broadly similar conclusions.
5. Performance is not entirely explained by one asset or one short period.
6. The limitations and failed cases can be explained clearly.

Failure to outperform is still a useful result if the experiment is reproducible and identifies why the original hypothesis was not supported.

## Expected Deliverables

- Reproducible configuration
- Validated dataset
- Tested strategy implementation
- Buy-and-hold baseline
- Metrics table
- Equity and drawdown plots
- Parameter-sensitivity analysis
- Final research report
- Documented limitations and next steps