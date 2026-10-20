"""Visualize product category profitability from the exported CSV."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "category_profitability.csv"
OUTPUT_FILE = ROOT / "outputs" / "category_profit_margin.png"


def main():
    with INPUT_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        records = list(csv.DictReader(file))

    if not records:
        raise ValueError("The category profitability CSV is empty.")

    records.sort(key=lambda row: float(row["Profit Margin (%)"]))

    categories = [row["Category"] for row in records]
    margins = [float(row["Profit Margin (%)"]) for row in records]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(categories, margins)

    ax.set_title(
        "Profit Margin by Product Category",
        fontsize=16,
        pad=18,
    )
    ax.set_xlabel("Profit Margin (%)")
    ax.set_xlim(0, max(margins) * 1.2)

    for bar, margin in zip(bars, margins):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{margin:.2f}%",
            va="center",
            fontsize=11,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
