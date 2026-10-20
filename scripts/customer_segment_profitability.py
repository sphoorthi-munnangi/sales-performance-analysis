"""Analyze historical profitability and discounts by RFM customer segment."""

from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from customer_segmentation import REFERENCE_DATE, assign_segment


def main():
    orders = pd.read_excel(
        ROOT / "Data" / "sample_-_superstore.xlsx",
        sheet_name="Orders",
    )
    orders["Order Date"] = pd.to_datetime(orders["Order Date"])

    customers = orders.groupby("Customer ID").agg(
        last_order=("Order Date", "max"),
        frequency=("Order ID", "nunique"),
        monetary=("Sales", "sum"),
        profit=("Profit", "sum"),
    )

    customers["recency"] = (
        REFERENCE_DATE - customers["last_order"]
    ).dt.days

    if (customers["recency"] < 0).any():
        raise ValueError("Reference date precedes some orders.")

    for score, column, ascending in [
        ("R", "recency", False),
        ("F", "frequency", True),
        ("M", "monetary", True),
    ]:
        customers[score] = pd.qcut(
            customers[column].rank(
                method="first",
                ascending=ascending,
            ),
            5,
            labels=[1, 2, 3, 4, 5],
        ).astype(int)

    customers["segment"] = customers.apply(
        assign_segment, axis=1
    )
    customers["unprofitable"] = customers["profit"] < 0

    summary = customers.groupby("segment").agg(
        customers=("monetary", "size"),
        sales=("monetary", "sum"),
        profit=("profit", "sum"),
        unprofitable_customers=("unprofitable", "sum"),
    )

    summary["profit_margin_pct"] = (
        summary["profit"] / summary["sales"] * 100
    )
    summary["unprofitable_customer_pct"] = (
        summary["unprofitable_customers"]
        / summary["customers"] * 100
    )

    transactions = orders.merge(
        customers[["segment"]],
        left_on="Customer ID",
        right_index=True,
        validate="many_to_one",
    )

    discounts = transactions.groupby("segment").agg(
        line_items=("Discount", "size"),
        avg_discount=("Discount", "mean"),
    )
    discounts["avg_discount_pct"] = (
        discounts["avg_discount"] * 100
    )

    summary = summary.join(
        discounts[["line_items", "avg_discount_pct"]]
    ).sort_values("sales", ascending=False)

    at_risk = transactions.loc[
        transactions["segment"] == "At-risk high-value"
    ]

    categories = at_risk.groupby("Category").agg(
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        line_items=("Sales", "size"),
    )
    categories["profit_margin_pct"] = (
        categories["profit"] / categories["sales"] * 100
    )

    assert summary["customers"].sum() == 804
    assert abs(summary["sales"].sum() - orders["Sales"].sum()) < 0.01
    assert abs(summary["profit"].sum() - orders["Profit"].sum()) < 0.01

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    summary.to_csv(
        output_dir / "customer_segment_profitability.csv",
        float_format="%.4f",
    )
    categories.to_csv(
        output_dir / "at_risk_category_profitability.csv",
        float_format="%.4f",
    )

    print("CUSTOMER SEGMENT PROFITABILITY")
    print("-" * 80)
    print(summary.round(2).to_string())

    print("\nAT-RISK CATEGORY PROFITABILITY")
    print("-" * 80)
    print(categories.round(2).to_string())

    print("\nVALIDATION")
    print(f"Customers: {summary['customers'].sum():,}")
    print(f"Sales: ${summary['sales'].sum():,.2f}")
    print(f"Profit: ${summary['profit'].sum():,.2f}")
    print("\nSaved both CSV reports to outputs/")


if __name__ == "__main__":
    main()
