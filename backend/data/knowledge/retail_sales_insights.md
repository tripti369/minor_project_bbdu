# Retail & Warehouse Sales — Business Notes

Dataset: retail_warehouse_sales_cleaned.csv (30,000 transaction rows, 2020)

Retail sales revenue is dominated by three categories: Liquor (~$81.7K),
Wine (~$59.7K) and Beer (~$59.5K) account for almost all retail revenue.
Non-alcohol, store supplies, refrigerated goods, kegs and dunnage
together make up a very small share of total sales, so forecasting effort
should focus on the liquor/wine/beer product lines — that is where
revenue volatility actually matters.

Because the sample only spans a handful of months within a single year,
short-term forecasts (the built-in Forecasting Agent) rely on a
weighted-moving-average fallback rather than full seasonal Holt-Winters
decomposition, since Holt-Winters needs at least two full seasonal
cycles of data to fit reliably. Once more months of data are ingested
(via the Upload page), the Forecasting Agent will automatically switch
to the seasonal model.

## Scenario simulation context

The Scenario Simulator (Monte Carlo) uses the sum of real retail_sales
from this dataset as its base revenue figure, then perturbs it with
user-supplied growth rate, pricing elasticity and cost-inflation
assumptions to produce a distribution of likely outcomes and a 95% Value
at Risk (VaR) figure. A wider VaR band means the business should hold
more cash buffer before committing to the scenario.

## Recommended actions

- Prioritise supply-chain and pricing analysis for liquor, wine and beer
  — they are the categories that actually move total revenue.
- Feed additional months of retail data into the system (via Upload) to
  unlock full seasonal forecasting instead of the moving-average
  fallback.
