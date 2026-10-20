"""Analyze high-discount prevalence and profitability in Central."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "central_discount_summary.csv"

SUBCATEGORIES = ["Appliances", "Binders", "Furnishings"]
HIGH_DISCOUNT_THRESHOLD = 0.60


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")

    central = orders.loc[
        (orders["Region"] == "Central")
        & (orders["Sub-Category"].isin(SUBCATEGORIES))
    ].copy()

    central["high_discount"] = (
        central["Discount"] >= HIGH_DISCOUNT_THRESHOLD
    )

    summary = (
        central.groupby("Sub-Category")
        .agg(
            total_items=("Row ID", "count"),
            high_discount_items=("high_discount", "sum"),
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
        )
        .reset_index()
    )

    summary["high_discount_share_pct"] = (
        summary["high_discount_items"]
        / summary["total_items"] * 100
    )

    summary["profit_margin_pct"] = (
        summary["total_profit"]
        / summary["total_sales"] * 100
    )

    summary = summary.sort_values("total_profit")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_FILE, index=False)

    print("CENTRAL HIGH-DISCOUNT SUMMARY")
    print("-" * 75)

    print(
        summary[
            [
                "Sub-Category",
                "total_items",
                "high_discount_items",
                "high_discount_share_pct",
                "total_profit",
                "profit_margin_pct",
            ]
        ].to_string(
            index=False,
            formatters={
                "high_discount_share_pct": "{:.1f}%".format,
                "total_profit": "${:,.2f}".format,
                "profit_margin_pct": "{:.2f}%".format,
            },
        )
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
