"""Visualize Central's high-discount prevalence and profitability."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "central_discount_summary.csv"
OUTPUT_FILE = ROOT / "outputs" / "central_discount_analysis.png"

NAVY = "#14263d"
TEAL = "#0f766e"
RED = "#b45353"


def main():
    data = pd.read_csv(INPUT_FILE)

    data = data.sort_values(
        "high_discount_share_pct",
        ascending=True,
    )

    categories = data["Sub-Category"]
    discount_shares = data["high_discount_share_pct"]
    profits = data["total_profit"]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12, 5.5)
    )

    bars1 = ax1.barh(categories, discount_shares, color=TEAL)
    ax1.set_title("High-Discount Prevalence", fontsize=13, color=NAVY)
    ax1.set_xlabel("Line items discounted 60% or more (%)")
    ax1.set_xlim(0, 85)

    for bar, value in zip(bars1, discount_shares):
        ax1.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
        )

    bars2 = ax2.barh(categories, profits, color=RED)
    ax2.set_title("Overall Subcategory Profit", fontsize=13, color=NAVY)
    ax2.set_xlabel("Net profit ($)")
    ax2.set_xlim(min(profits) * 1.45, 0)

    for bar, value in zip(bars2, profits):
        ax2.text(
            value - 80,
            bar.get_y() + bar.get_height() / 2,
            f"-${abs(value):,.0f}",
            ha="right",
            va="center",
        )

    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", alpha=0.15)
        ax.set_axisbelow(True)

    fig.suptitle(
        "Central Region: High Discounts and Profitability",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
    )

    fig.text(
        0.5, 0.01,
        "High discount = 60% or more. Profit includes all discount levels.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.05, 1, 0.92])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
