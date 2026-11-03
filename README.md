# Olist E-commerce Data Analysis & BI Dashboard

> Which delivery outcomes, seller and category cohorts, and customer segments are associated with poor reviews, and where should operations investigate first?

This project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The customer-experience analysis complements the existing sales dashboard with reproducible order-level metrics and Power BI-ready tables.

- [Existing sales dashboard (PDF)](powerbi/Olist_Dashboard.pdf) · [Power BI file](powerbi/Olist_Dashboard.pbix)
- [Exploratory notebook](notebooks/EDA_Olist.ipynb) · [Customer-experience Power BI build guide](powerbi/customer_experience.md)

## Run the analysis

Clone this repository, create a Python environment, and extract the original Olist CSVs into `data/raw/`. Run these commands from the repository root:

```bash
python -m pip install -r requirements.txt
python -m src.pipeline
python -m src.customer_experience
```

The existing ETL writes Parquet tables to `data/processed/`. The customer-experience module runs independently and writes CSVs to `data/processed/experience/`. To use another dataset or output directory, pass `--raw-dir` or `--output-dir`.

## Analysis and decisions

| Question | Evidence to compare | Decision |
| --- | --- | --- |
| Do customers report worse experiences when delivery is slow or late? | 1–2 star rates by delivery outcome and elapsed time, with reviewed-order counts | Review promised-date SLA and investigate high-volume late cohorts |
| Where is the problem concentrated? | Late rates and order volumes by customer state, plus negative-review rates by seller and category | Prioritize cohorts with both substantial volume and elevated rates |
| Which customers warrant a closer look? | Review rates, customer counts, and merchandise value by buyer segment | Compare repeat buyers and high-value first-time buyers before designing retention actions |

### Measurement rules

- Use one row per order for platform KPIs. If an order has multiple valid reviews, use the latest answer timestamp and break ties by review ID. A negative review scores 1–2 out of 5. The denominator is reviewed orders.
- Late deliveries are delivered orders with valid elapsed time and both delivery and estimated dates, delivered after the promised calendar day. Missing delivery dates are excluded from the rate. Delivery duration is measured from purchase in elapsed days.
- Merchandise value in BRL sums item prices, excluding freight. The order-level export includes all statuses, so filter to delivered for a delivered merchandise-value KPI. Merchandise value is distinct from the sum of payment records.
- Buyer segments are fixed across the full delivered-order history. Repeat buyers have at least two delivered orders. High-value one-time buyers have one delivered order and spend at or above the 75th percentile of delivered buyers' merchandise spend.
- Seller and category rates use one row per order–entity pair. The same order review can inform multiple sellers or categories. The aggregate quality exports require at least 50 reviewed orders per seller and 100 per category. These are screening signals and may reflect delivery or other factors outside seller control.

The customer-experience exports and page specifications are available in this repository. The linked PBIX and PDF are the existing sales report. Findings should come from running this project's analysis on the source data. The comparisons are descriptive and do not establish causation.

The business-question approach was inspired by [Gia Vy's Olist customer dissatisfaction case study](https://www.facebook.com/groups/nguoilamdata/permalink/3541524962688518/).
