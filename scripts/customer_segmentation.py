"""Create reproducible RFM customer segments and an aggregate summary."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "customer_segments_summary.csv"

REFERENCE_DATE = pd.Timestamp("2026-12-31")


def assign_segment(row):
    """Assign one mutually exclusive business segment."""
    r, f, m = row["R"], row["F"], row["M"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    if r <= 2 and f >= 4 and m >= 4:
        return "At-risk high-value"

    if r >= 3 and f >= 4:
        return "Loyal customers"

    if r >= 4 and f <= 3:
        return "Potential loyalists"

    return "Other customers"


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")
    orders["Order Date"] = pd.to_datetime(orders["Order Date"])

    rfm = (
        orders.groupby("Customer ID")
        .agg(
            last_order=("Order Date", "max"),
            frequency=("Order ID", "nunique"),
            monetary=("Sales", "sum"),
        )
    )

    rfm["recency"] = (
        REFERENCE_DATE - rfm["last_order"]
    ).dt.days

    if (rfm["recency"] < 0).any():
        raise ValueError(
            "Reference date precedes some customer orders."
        )

    # Rank-based quintiles handle ties deterministically.
    # Scores are relative to this dataset, not universal thresholds.
    rfm["R"] = pd.qcut(
        rfm["recency"].rank(method="first", ascending=False),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    rfm["F"] = pd.qcut(
        rfm["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    rfm["M"] = pd.qcut(
        rfm["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)

    rfm["segment"] = rfm.apply(assign_segment, axis=1)

    summary = (
        rfm.groupby("segment")
        .agg(
            customers=("monetary", "size"),
            total_revenue=("monetary", "sum"),
            avg_recency=("recency", "mean"),
            avg_orders=("frequency", "mean"),
            avg_spending=("monetary", "mean"),
        )
    )

    summary["customer_share_pct"] = (
        summary["customers"] / len(rfm) * 100
    )

    summary["revenue_share_pct"] = (
        summary["total_revenue"] / rfm["monetary"].sum() * 100
    )

    summary = summary.sort_values(
        "total_revenue", ascending=False
    )

    # Validate that no customers or revenue were omitted.
    assert summary["customers"].sum() == len(rfm)
    assert abs(
        summary["total_revenue"].sum()
        - orders["Sales"].sum()
    ) < 0.01

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_FILE, float_format="%.4f")

    print("CUSTOMER SEGMENTATION SUMMARY")
    print("-" * 90)

    columns = [
        "customers",
        "customer_share_pct",
        "revenue_share_pct",
        "avg_recency",
        "avg_orders",
        "avg_spending",
    ]

    print(summary[columns].round(1).to_string())

    print("\nVALIDATION")
    print(f"Total customers: {summary['customers'].sum():,}")
    print(f"Total revenue: ${summary['total_revenue'].sum():,.2f}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
