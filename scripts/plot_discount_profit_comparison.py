"""Compare profit from high-discount and other Central transactions."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "discount_profit_comparison.png"

SUBCATEGORIES = ["Furnishings", "Appliances", "Binders"]

NAVY = "#14263d"
TEAL = "#0f766e"
RED = "#b45353"


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")

    data = orders.loc[
        (orders["Region"] == "Central")
        & (orders["Sub-Category"].isin(SUBCATEGORIES))
    ].copy()

    data["Discount Group"] = np.where(
        data["Discount"] >= 0.60,
        "High discounts (60%+)",
        "Other discounts (<60%)",
    )

    summary = (
        data.groupby(["Sub-Category", "Discount Group"])["Profit"]
        .sum()
        .unstack(fill_value=0)
        .reindex(SUBCATEGORIES)
    )

    high_profit = summary["High discounts (60%+)"]
    other_profit = summary["Other discounts (<60%)"]

    y = np.arange(len(SUBCATEGORIES))
    bar_height = 0.32

    fig, ax = plt.subplots(figsize=(11, 6))

    high_bars = ax.barh(
        y - bar_height / 2,
        high_profit,
        height=bar_height,
        color=RED,
        label="High discounts (60%+)",
    )

    other_bars = ax.barh(
        y + bar_height / 2,
        other_profit,
        height=bar_height,
        color=TEAL,
        label="Other discounts (<60%)",
    )

    ax.axvline(0, color=NAVY, linewidth=1.2)

    ax.set_yticks(y)
    ax.set_yticklabels(SUBCATEGORIES, fontsize=12)
    ax.invert_yaxis()

    ax.set_xlabel("Total profit ($)", fontsize=11)

    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"${value / 1000:,.0f}k")
    )

    ax.set_title(
        "Central Region: Profit by Discount Group",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=22,
    )

    for bars in (high_bars, other_bars):
        for bar in bars:
            value = bar.get_width()

            if value < 0:
                x = value - 350
                alignment = "right"
                label = f"−${abs(value):,.0f}"
            else:
                x = value + 350
                alignment = "left"
                label = f"+${value:,.0f}"

            ax.text(
                x,
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                ha=alignment,
                fontsize=10,
                color=NAVY,
            )

    ax.set_xlim(
        min(high_profit.min(), other_profit.min()) * 1.25,
        max(high_profit.max(), other_profit.max()) * 1.25,
    )

    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, -0.23),
        ncol=2,
        frameon=False,
    )

    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.text(
        0.5,
        0.02,
        "Observed profit by transaction discount group; "
        "not an estimate of profit recoverable from changing prices.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.08, 1, 1])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("CENTRAL — PROFIT BY DISCOUNT GROUP")
    print("-" * 65)
    print(summary.to_string(float_format=lambda x: f"${x:,.2f}"))
    print(f"\nChart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
