"""Reproducible sales and profitability analysis for Sample Superstore."""

from collections import defaultdict
from pathlib import Path

import openpyxl


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "Data" / "sample_-_superstore.xlsx"


def load_orders():
    """Read the original Orders worksheet without modifying the workbook."""
    workbook = openpyxl.load_workbook(
        DATA_PATH,
        read_only=True,
        data_only=True,
    )

    try:
        worksheet = workbook["Orders"]
        rows = worksheet.iter_rows(values_only=True)
        headers = next(rows)

        return [
            dict(zip(headers, values))
            for values in rows
        ]
    finally:
        workbook.close()


def summarize_sales(orders):
    """Calculate overall sales, profitability, and customer KPIs."""
    sales = sum(float(row["Sales"]) for row in orders)
    profit = sum(float(row["Profit"]) for row in orders)
    order_ids = {row["Order ID"] for row in orders}
    customer_ids = {row["Customer ID"] for row in orders}

    print("\nOVERALL BUSINESS PERFORMANCE")
    print("-" * 45)
    print(f"Sales line items: {len(orders):,}")
    print(f"Total sales: ${sales:,.2f}")
    print(f"Total profit: ${profit:,.2f}")
    print(f"Profit margin: {profit / sales:.2%}")
    print(f"Distinct orders: {len(order_ids):,}")
    print(f"Unique customers: {len(customer_ids):,}")
    print(f"Average order value: ${sales / len(order_ids):,.2f}")


def summarize_categories(orders):
    """Compare sales and profit across product categories."""
    categories = defaultdict(lambda: {"sales": 0.0, "profit": 0.0})

    for row in orders:
        category = row["Category"]
        categories[category]["sales"] += float(row["Sales"])
        categories[category]["profit"] += float(row["Profit"])

    print("\nCATEGORY PROFITABILITY")
    print("-" * 75)
    print(f"{'Category':<20}{'Sales':>18}{'Profit':>18}{'Margin':>12}")

    for category, values in sorted(categories.items()):
        margin = values["profit"] / values["sales"]

        print(
            f"{category:<20}"
            f"${values['sales']:>17,.2f}"
            f"${values['profit']:>17,.2f}"
            f"{margin:>11.2%}"
        )


def analyze_table_discounts(orders):
    """Analyze Tables profitability across mutually exclusive discount bands."""
    bands = [
        ("0%", lambda discount: discount == 0),
        ("Above 0% to 20%", lambda discount: 0 < discount <= 0.20),
        ("Above 20% to 40%", lambda discount: 0.20 < discount <= 0.40),
        ("Above 40%", lambda discount: discount > 0.40),
    ]

    tables = [
        row for row in orders
        if row["Sub-Category"] == "Tables"
    ]

    print("\nTABLES PROFITABILITY BY DISCOUNT")
    print("-" * 85)
    print(
        f"{'Discount band':<22}"
        f"{'Rows':>7}"
        f"{'Sales':>17}"
        f"{'Profit':>17}"
        f"{'Margin':>11}"
        f"{'Loss %':>10}"
    )

    for label, condition in bands:
        selected = [
            row for row in tables
            if condition(float(row["Discount"]))
        ]

        if not selected:
            continue

        sales = sum(float(row["Sales"]) for row in selected)
        profit = sum(float(row["Profit"]) for row in selected)
        loss_count = sum(float(row["Profit"]) < 0 for row in selected)

        print(
            f"{label:<22}"
            f"{len(selected):>7,}"
            f"${sales:>16,.2f}"
            f"${profit:>16,.2f}"
            f"{profit / sales:>10.2%}"
            f"{loss_count / len(selected):>9.2%}"
        )

    print(f"\nTotal Tables line items: {len(tables):,}")
    print(
        "Total Tables profit: "
        f"${sum(float(row['Profit']) for row in tables):,.2f}"
    )


def main():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    orders = load_orders()
    summarize_sales(orders)
    summarize_categories(orders)
    analyze_table_discounts(orders)


if __name__ == "__main__":
    main()
