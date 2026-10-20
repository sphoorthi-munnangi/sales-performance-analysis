"""Decompose the 2025–2026 change in profit margin by category."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "margin_decomposition.csv"

BASE_YEAR = 2025
COMPARISON_YEAR = 2026


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")
    orders["Year"] = pd.to_datetime(orders["Order Date"]).dt.year

    data = orders.loc[
        orders["Year"].isin([BASE_YEAR, COMPARISON_YEAR])
    ]

    summary = (
        data.groupby(["Category", "Year"])
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
    )

    sales = summary["sales"].unstack("Year")
    profit = summary["profit"].unstack("Year")

    shares = sales.div(sales.sum(axis=0), axis=1)
    margins = profit / sales

    within = (
        (margins[COMPARISON_YEAR] - margins[BASE_YEAR])
        * (shares[BASE_YEAR] + shares[COMPARISON_YEAR]) / 2
    )

    mix = (
        (shares[COMPARISON_YEAR] - shares[BASE_YEAR])
        * (margins[BASE_YEAR] + margins[COMPARISON_YEAR]) / 2
    )

    result = pd.DataFrame({
        "category": sales.index,
        "within_effect_pp": within.values * 100,
        "sales_mix_effect_pp": mix.values * 100,
        "total_effect_pp": (within + mix).values * 100,
    })

    actual_change = (
        profit[COMPARISON_YEAR].sum()
        / sales[COMPARISON_YEAR].sum()
        - profit[BASE_YEAR].sum()
        / sales[BASE_YEAR].sum()
    ) * 100

    calculated_change = result["total_effect_pp"].sum()

    if abs(actual_change - calculated_change) > 1e-9:
        raise ValueError("Decomposition does not match actual change.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("PROFIT MARGIN DECOMPOSITION")
    print("-" * 70)
    print(result.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))

    print(f"\nWithin-category effect: {within.sum() * 100:+.3f} pp")
    print(f"Sales-mix effect:       {mix.sum() * 100:+.3f} pp")
    print(f"Total margin change:    {actual_change:+.3f} pp")
    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
