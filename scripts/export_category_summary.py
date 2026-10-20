"""Export category-level sales and profitability metrics to CSV."""

import csv
from collections import defaultdict
from pathlib import Path

import openpyxl


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "category_profitability.csv"


def main():
    workbook = openpyxl.load_workbook(
        DATA_FILE,
        read_only=True,
        data_only=True,
    )

    try:
        worksheet = workbook["Orders"]
        rows = worksheet.iter_rows(values_only=True)
        headers = next(rows)
        indexes = {name: i for i, name in enumerate(headers)}

        categories = defaultdict(
            lambda: {
                "sales": 0.0,
                "profit": 0.0,
                "line_items": 0,
                "loss_items": 0,
            }
        )

        for row in rows:
            category = row[indexes["Category"]]
            sales = float(row[indexes["Sales"]])
            profit = float(row[indexes["Profit"]])

            summary = categories[category]
            summary["sales"] += sales
            summary["profit"] += profit
            summary["line_items"] += 1
            summary["loss_items"] += int(profit < 0)

    finally:
        workbook.close()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Category",
            "Total Sales",
            "Total Profit",
            "Profit Margin (%)",
            "Line Items",
            "Loss-Making Items",
            "Loss Rate (%)",
        ])

        for category, values in sorted(categories.items()):
            sales = values["sales"]
            profit = values["profit"]
            count = values["line_items"]

            writer.writerow([
                category,
                round(sales, 2),
                round(profit, 2),
                round(profit / sales * 100, 2),
                count,
                values["loss_items"],
                round(values["loss_items"] / count * 100, 2),
            ])

    print(f"CSV created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
