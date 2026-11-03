# Build the customer-experience report in Power BI

Run `python -m src.customer_experience` from the repository root. In Power BI Desktop import the CSVs in `data/processed/experience/`. Set the three timestamp columns to Date/Time, review score and indicator flags to numbers, and monetary fields to Decimal Number. Use BRL for merchandise value.

Use `order_experience` as the primary table. For seller and category views, create single-direction one-to-many relationships from its `order_id` to `seller_order_experience[order_id]` and `category_order_experience[order_id]`. The summary CSVs are independent outputs for QA and fixed cohort views. Interactive order-level filters should use the detail tables.

## Core measures

```dax
Orders = COUNTROWS(order_experience)
Reviewed Orders = COUNT(order_experience[negative_review])
Negative Reviews = SUM(order_experience[negative_review])
Negative Review Rate = DIVIDE([Negative Reviews], [Reviewed Orders])
Measured Deliveries = COUNT(order_experience[late_delivery])
Late Delivery Rate = DIVIDE(SUM(order_experience[late_delivery]), [Measured Deliveries])
Avg Review Score = AVERAGE(order_experience[review_score])
Delivered Merchandise Value BRL =
    CALCULATE(SUM(order_experience[item_value_brl]), order_experience[order_status] = "delivered")
```

For seller visuals, count and sum the indicators from the related order row in the context of the seller detail table. Use the same pattern for category visuals by substituting the category table:

```dax
Seller Reviewed Orders =
    COUNTX(seller_order_experience, RELATED(order_experience[negative_review]))
Seller Negative Review Rate =
    DIVIDE(
        SUMX(seller_order_experience, RELATED(order_experience[negative_review])),
        [Seller Reviewed Orders]
    )
```

An order may appear under several sellers or categories, so hide grand totals for those rates. Use blank denominators as blanks, not zero rates.

## Six report pages

| Page | Visuals | Decision supported |
| --- | --- | --- |
| Executive Overview | Orders, delivered merchandise value, negative-review and late rates, monthly trends | Spot changes in volume and operational health |
| Customer Priority Segmentation | Buyer counts from `customer_segments`, order review rates and delivered merchandise value by segment | Select cohorts for retention or service follow-up |
| Customer Satisfaction | Review score distribution and trend, review rates by outcome, state comparison | Identify when and where dissatisfaction is concentrated |
| Delivery Performance | Review rate and sample size by delivery band, late rate by month and state | Select lanes or periods for SLA investigation |
| Seller & Product Quality | Scatter plots by reviewed-order count and negative-review rate, seller and category tables | Screen cohorts for investigation with minimum sample sizes |
| Recommendations | Evidence, proposed action, owner, and follow-up KPI | Translate observed patterns into actions to validate |

Use a consistent left navigation rail and orange for callouts. On operational pages use shared month, customer state and segment slicers. Mark buyer counts from the segment summary as full-history metrics. Include reviewed-order counts beside rates and annotate whether the denominator is reviewed orders or measured deliveries.

## Decision rules to apply after refresh

- Investigate SLA alerts where late rate and late-order counts are both high. Track late rate and 1–2 star rate after a pilot.
- Review sellers with high negative-review rates and sufficient reviewed orders. Inspect representative cases for logistics or product issues before attributing the problem to the seller.
- Compare repeat buyers with high-value one-time buyers before assigning retention resources. Track both review rate and delivered merchandise value.
