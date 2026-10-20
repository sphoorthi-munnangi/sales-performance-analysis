# Sales Performance Analysis — Research Findings

## Project objective

Investigate sales performance, profitability, discounting,
and regional differences using the Sample Superstore dataset.

## Dataset

- Source worksheet: Orders
- Sales line items: 10,194
- Distinct orders: 5,111
- Unique customers: 804
- Order dates: January 2023 to December 2026
- Dataset treated as a practice case study, not live business data.

## Data quality

- No missing values across the 21 Orders columns.
- No exact duplicate rows.
- No duplicate Row IDs.
- Positive sales and quantities.
- Discounts within the range 0 to 100%.
- No shipments dated before their orders.
- 1,901 loss-making line items.

## Overall performance

- Total sales: $2,326,534.35
- Total profit: $292,296.81
- Overall profit margin: 12.56%
- Average order value: $455.20

## Finding 1 — Furniture has a low profit margin

Furniture generated $754,747.76 in sales but only $19,730
in profit, giving a margin of 2.61%.

Technology and Office Supplies had profit margins above 17%.

## Finding 2 — Tables and Bookcases are unprofitable

Tables:
- Sales: $208,020.18
- Profit: -$17,753.21
- Profit margin: -8.53%

Bookcases:
- Sales: $115,361.20
- Profit: -$3,632.07
- Profit margin: -3.15%

## Finding 3 — Tables profitability varies by discount level

| Discount band | Line items | Profit margin |
|---|---:|---:|
| 0% | 76 | 18.60% |
| Above 0% to 20% | 72 | -0.65% |
| Above 20% to 40% | 131 | -27.52% |
| Above 40% | 47 | -57.98% |

All 47 Tables line items discounted above 40%
generated negative profit.

## Finding 4 — Central Furniture is unprofitable

Central Furniture:
- Sales: $164,537.65
- Profit: -$2,802.21
- Profit margin: -1.70%
- Loss-making line-item rate: 65.77%

Three Central Furniture subcategories generated
negative overall profit: Furnishings, Tables, and Bookcases.

## Finding 5 — Central Furnishings have unusually high discounts

| Region | Profit margin | Average discount |
|---|---:|---:|
| Central | -25.62% | 40.39% |
| East | 19.93% | 8.58% |
| South | 19.89% | 10.67% |
| West | 25.55% | 3.41% |

Central also had a 67.63% loss-making line-item rate
for Furnishings, substantially higher than other regions.

## Interpretation and limitations

Higher discounts are associated with lower profitability
in several observed comparisons.

These descriptive analyses do not establish causation.
Differences in product mix, costs, customer segments,
geography, and other factors may contribute.

No pricing-policy change should be recommended solely
on the basis of these comparisons.

## Next investigations

1. Examine discount distributions and product mix.
2. Test associations using appropriate statistical methods.
3. Analyze sales and profit trends over time.
4. Join Returns data and investigate return patterns.
5. Develop evidence-based business recommendations.

## Finding 6 — Matched-product discount comparison

We identified 122 Furnishings products sold in Central and
at least one other region.

Among these shared products:

- Central sales line items: 205
- Other-region sales line items: 517
- Central profit margin: -25.27%
- Other-region profit margin: 20.45%
- Central average discount: 40.20%
- Other-region average discount: 7.60%

These are pooled transaction-level summaries restricted
to matched product IDs, not paired estimates of profit.

## Finding 7 — Statistical test of regional discount differences

For each matched product, we compared its average discount
in Central with its average discount outside Central.

- Matched products: 122
- Higher average discount in Central: 96
- Equal average discount: 7
- Lower average discount in Central: 19
- Mean within-product difference: +33.75 percentage points
- Median within-product difference: +45.00 percentage points

### Exact binomial sign test

Null hypothesis:
Among products with unequal average discounts, Central
is equally likely to have a higher or lower discount.

Alternative hypothesis:
Central is more likely to have a higher discount.

- Non-tied product comparisons: 115
- One-sided p-value: 7.234e-14
- Significance level: 0.05
- Decision: Reject the null hypothesis.

### Interpretation

There is strong statistical evidence that Central tends
to apply higher discounts to matched Furnishings products.

This test does not establish that discounts caused
profitability differences.

Limitations include possible dependence among products,
unequal transaction counts, time effects, and unmeasured
differences in customer or transaction characteristics.

The hypothesis was developed after exploratory analysis,
so the result should be presented as exploratory inference,
not as a preregistered confirmatory test.

## Finding 8 — High-discount losses extend beyond Furniture

Central's transactions discounted by at least 60% include
three subcategories with substantial losses:

| Subcategory | High-discount items | High-discount profit |
|---|---:|---:|
| Binders | 236 | -$21,955.06 |
| Appliances | 67 | -$8,629.64 |
| Furnishings | 139 | -$5,950.96 |

Combined profit across these 442 high-discount line items
was -$36,535.66.

The observed high discount levels were:
- Binders: 70% and 80%
- Appliances: 80%
- Furnishings: 60%

## Finding 9 — High discounts are widespread in Central

| Subcategory | Share of line items discounted 60%+ | Overall profit |
|---|---:|---:|
| Furnishings | 67.1% | -$3,915.52 |
| Appliances | 54.5% | -$2,638.62 |
| Binders | 63.4% | -$958.31 |

All three subcategories were unprofitable overall in Central.

Profitable transactions at other discount levels offset
some of the losses from heavily discounted transactions.

## Business interpretation

Central's heavily discounted transactions warrant further
investigation, particularly the 80% discounts on Binders
and Appliances and the 60% discounts on Furnishings.

These are observational findings. The recorded losses
should not be interpreted as recoverable profit from
reducing discounts because customer demand could change.

## Visualization

See outputs/central_discount_analysis.png.

The chart compares high-discount prevalence with overall
subcategory profitability. Overall profit includes
transactions at every discount level.

## Finding 10 — Profitable transactions offset high-discount losses

A comparison of Central's profit by discount group reveals:

| Subcategory | Profit at discounts 60%+ | Profit at discounts below 60% |
|---|---:|---:|
| Furnishings | -$5,950.96 | +$2,035.44 |
| Appliances | -$8,629.64 | +$5,991.02 |
| Binders | -$21,955.06 | +$20,996.75 |

Binders provide the clearest example of offsetting performance.
Despite approximately $21,955 in losses on heavily discounted
transactions, profits from other transactions reduced the
subcategory's overall net loss to approximately $958.

This finding demonstrates why analyzing only total subcategory
profit can conceal substantial losses within particular
transaction groups.

Visualization: outputs/discount_profit_comparison.png

These figures describe observed profit contributions, not
the financial effect of changing discount policies.

## Finding 11 — Understanding the 2026 Profit Margin Decline

Annual sales increased by 21.4% in 2026, while profit increased
by 16.0%. The overall profit margin declined from 13.465% in
2025 to 12.866% in 2026, a decrease of 0.599 percentage points.

A symmetric margin decomposition separated this change into:

| Component | Contribution |
|---|---:|
| Within-category margin changes | -1.103 pp |
| Changes in category sales mix | +0.504 pp |
| Net change | -0.599 pp |

### Category-Level Findings

- Furniture: Declining category profitability contributed
  -0.641 pp through the within-category effect.
- Office Supplies: Declining category profitability contributed
  -0.858 pp, partly offset by a +0.656 pp sales-mix effect.
- Technology: Improving category profitability contributed
  +0.396 pp through the within-category effect.

### Business Interpretation

The overall margin decline was primarily associated with
deteriorating profitability within Furniture and Office Supplies.

Changes in the distribution of sales across categories partially
offset these declines.

The results suggest that investigating category-level pricing,
discounts, product mix, and costs may be more useful than
focusing on total sales growth alone.

### Methodology and Limitations

The analysis uses a symmetric two-period accounting decomposition.
It exactly reconciles the observed change in overall profit margin.

The contributions are descriptive, not causal. The analysis
does not establish why individual category margins changed.

Supporting files:
- scripts/margin_decomposition.py
- outputs/margin_decomposition.csv
- scripts/plot_margin_drivers.py
- outputs/margin_drivers.png

## Finding 12 — Seasonal Sales Patterns and Profitability

Monthly sales were analyzed across 2023–2026 using an index
that compares each month's revenue with the average monthly
revenue within its own year.

### Seasonal Demand

The strongest average monthly sales indices were:

- November: 182.5
- December: 173.6
- September: 162.6

The weakest were:

- February: 29.7
- January: 47.5

November, December, and September exceeded their respective
annual monthly averages in all four years.

These results suggest recurring seasonal sales patterns.

### Sales Versus Profitability

Across the four years:

| Month | Total Sales | Total Profit | Profit Margin |
|---|---:|---:|---:|
| September | $308,883.67 | $37,234.56 | 12.05% |
| November | $352,665.99 | $35,541.26 | 10.08% |
| December | $330,218.18 | $44,229.85 | 13.39% |

November generated the highest revenue, but December
generated approximately $8,689 more profit.

The overall profit margin was 12.56%, meaning November
and September performed below the overall margin despite
their high sales volumes.

### Business Implications

Seasonal demand patterns may inform inventory planning,
staffing, and promotional scheduling.

However, peak revenue does not necessarily correspond
to peak profitability. Additional analysis of product mix,
discounting, and regional performance is needed before
recommending changes to promotional strategies.

### Limitations

The analysis uses four years of sample retail data.
The seasonal patterns are descriptive and do not constitute
validated forecasts.

The monthly profitability chart aggregates each calendar
month across all four years and does not show year-specific
variation.

Supporting files:
- scripts/plot_monthly_performance.py
- outputs/monthly_performance.png

## Finding 13 — Customer Purchasing Behavior and RFM Segmentation

The dataset contains 804 unique customers and 5,111 distinct
orders across 2023–2026.

### Customer Purchasing Behavior

- 792 customers (98.51%) placed more than one order.
- Average orders per customer: 6.36.
- Average customer revenue: $2,893.70.
- Median customer revenue: $2,243.39.
- The highest-spending 80 customers generated 30.87% of revenue.

The repeat-purchase percentage is not a formal retention rate.

### RFM Methodology

Customers were scored using:

- Recency: Days since their most recent order.
- Frequency: Number of distinct orders.
- Monetary value: Total historical sales.

The reference date was December 31, 2026.

Each metric received a score from 1 to 5 using ranked
quintiles. Higher scores represent more recent purchasing,
more orders, or greater spending.

Rule-based segments were assigned using the individual
R, F, and M scores rather than only their combined total.

### Customer Segment Results

| Segment | Customers | Customer Share | Revenue Share |
|---|---:|---:|---:|
| Champions | 108 | 13.4% | 25.1% |
| Loyal customers | 132 | 16.4% | 16.1% |
| Potential loyalists | 152 | 18.9% | 14.9% |
| At-risk high-value | 55 | 6.8% | 13.4% |
| Other customers | 357 | 44.4% | 30.6% |

All 804 customers and 100% of historical revenue were
accounted for.

### Key Business Finding

The 55 at-risk high-value customers represented 6.8%
of customers but generated 13.4% of historical revenue.

Their average recency was approximately 206 days, and
their average historical spending was $5,658.

This group may be worth investigating for potential
re-engagement opportunities.

Champions also represent an important customer group:
13.4% of customers generated 25.1% of historical revenue.

### Business Recommendations

Potential next steps include:

- Investigating the purchasing patterns of high-value
  customers who have not ordered recently.
- Exploring retention and loyalty strategies for Champions.
- Encouraging repeat purchases among Potential loyalists.
- Evaluating segment profitability, not just revenue.

These are hypotheses for further business investigation,
not validated intervention strategies.

### Limitations

RFM segments are descriptive and rule-based.

The labels do not predict churn, future purchases, or
customer lifetime value.

Rank-based scoring can assign different scores to
customers with identical order frequencies.

Customer behavior is measured only within the available
sample dataset. No transactions after December 2026
are observed.

Supporting files:
- scripts/customer_segmentation.py
- outputs/customer_segments_summary.csv
- scripts/plot_customer_segments.py
- outputs/customer_segments.png

## Finding 14 — Customer Segment Profitability

Customer segments were evaluated using historical sales,
transaction profit, profit margin, and discounting.

### Key Results

| Segment | Profit | Profit Margin | Customers with Negative Net Profit |
|---|---:|---:|---:|
| Champions | $71,996.37 | 12.35% | 12.96% |
| Loyal customers | $38,700.08 | 10.35% | 15.91% |
| Potential loyalists | $49,678.32 | 14.32% | 22.37% |
| At-risk high-value | $56,728.19 | 18.23% | 10.91% |
| Other customers | $75,193.85 | 10.57% | 23.53% |

All 804 customers were included. Segment profits sum to
$292,296.81, matching total dataset profit.

### Main Finding

The 55 at-risk high-value customers accounted for:

- 6.8% of customers.
- 13.4% of historical revenue.
- 19.4% of historical transaction profit.

Their profit margin was 18.23%, the highest among the
five customer segments.

Their average transaction-line discount was 13.79%,
the lowest segment average.

### Product Category Findings

Within the at-risk high-value segment:

| Category | Profit | Profit Margin |
|---|---:|---:|
| Furniture | $6,293.22 | 6.33% |
| Office Supplies | $26,309.46 | 24.75% |
| Technology | $24,125.51 | 22.86% |

Office Supplies and Technology contributed approximately
89% of the segment's historical transaction profit.

### Business Implications

The at-risk high-value segment is a potential priority
for further customer-retention investigation because
it combines relatively high historical profitability
with less recent purchasing activity.

Possible next steps include:

- Investigating why these customers have not purchased recently.
- Examining their typical purchasing intervals.
- Evaluating whether targeted re-engagement campaigns
  could be cost-effective.
- Studying discounting and category mix in greater detail.

### Limitations

These findings are descriptive, not causal.

Lower average discounts do not necessarily explain
the higher profit margin.

The at-risk label is based on RFM rules, not a validated
churn prediction model.

Profit excludes customer acquisition and servicing costs.
Historical profitability does not guarantee future value.

Supporting files:
- scripts/customer_segment_profitability.py
- outputs/customer_segment_profitability.csv
- outputs/at_risk_category_profitability.csv
- scripts/plot_customer_profit_contribution.py
- outputs/customer_profit_contribution.png
