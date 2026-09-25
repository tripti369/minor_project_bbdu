# Customer Churn — Business Notes

Dataset: customer_churn_cleaned.csv (64,374 customers)

Overall churn rate is 47.4% across the customer base.

Churn by subscription tier: Basic 48.3%, Standard 47.3%, Premium 46.5%.
Premium subscribers churn slightly less than Basic subscribers, suggesting
that higher-value plans have somewhat stronger retention, though the gap
is small (under 2 points) and not enough on its own to justify a pricing
change.

Churn by contract length shows the clearest signal in this dataset:
Monthly contracts churn at 51.6%, Annual contracts at 46.2%, and Quarterly
contracts are the stickiest at 44.0%. This is the single strongest lever
in the data — customers on month-to-month billing are meaningfully more
likely to leave than customers locked into quarterly or annual terms.

Support calls are a leading indicator of churn risk: customers who
eventually churn average 6.4 support calls versus 4.5 for customers who
stay. A rising support-call count for an account is therefore a useful
early-warning signal for the retention team.

Average total spend is actually slightly *lower* for churned customers
($519) than retained customers ($560), which rules out "big spenders are
the ones leaving" as an explanation — churn is not concentrated in the
highest-value segment.

## Business forecasting risk

When forecast accuracy drops below 70%, treat the revenue and churn
projections as directional only, not decision-grade. Cross-check any
automated forecast against the most recent 2-3 months of actuals before
using it to justify budget or headcount changes. High churn (>45%)
combined with low forecast confidence is the highest-risk combination —
it means the business doesn't know how many customers it will have *and*
isn't sure how much each one will spend.

## Recommended actions

- Target monthly-contract customers with an incentive to move to
  quarterly or annual billing (the biggest churn-rate gap in the data).
- Flag accounts with 3+ support calls in a rolling 30-day window for a
  proactive retention outreach.
- Do not assume premium customers are safe from churn — the tier gap is
  small, so retention effort should be spread across all tiers.
