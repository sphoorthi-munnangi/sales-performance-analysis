"""Visualize revenue and profit contributions by customer segment."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "customer_segment_profitability.csv"
OUTPUT_FILE = ROOT / "outputs" / "customer_profit_contribution.png"

NAVY = "#14263d"
TEAL = "#0f766e"

ORDER = [
    "Champions",
    "Loyal customers",
    "Potential loyalists",
    "At-risk high-value",
    "Other customers",
]


def main():
    data = pd.read_csv(INPUT_FILE, index_col="segment")
    data = data.loc[ORDER].copy()

    data["revenue_share"] = (
        data["sales"] / data["sales"].sum() * 100
    )
    data["profit_share"] = (
        data["profit"] / data["profit"].sum() * 100
    )

    y = np.arange(len(data))
    height = 0.34

    fig, ax = plt.subplots(figsize=(11, 6.5))

    revenue_bars = ax.barh(
        y - height / 2,
        data["revenue_share"],
        height,
        color=NAVY,
        label="Revenue share",
    )

    profit_bars = ax.barh(
        y + height / 2,
        data["profit_share"],
        height,
        color=TEAL,
        label="Profit share",
    )

    for bars in (revenue_bars, profit_bars):
        for bar in bars:
            value = bar.get_width()
            ax.text(
                value + 0.4,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.1f}%",
                va="center",
                fontsize=10,
                color=NAVY,
            )

    ax.set_yticks(y, ORDER)
    ax.invert_yaxis()
    ax.set_xlim(0, 35)
    ax.set_xlabel("Share of total (%)")

    ax.set_title(
        "Customer Segments: Revenue vs. Profit Contribution",
        fontsize=16,
        fontweight="bold",
        color=NAVY,
        pad=20,
    )

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        frameon=False,
    )

    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)

    fig.text(
        0.5,
        0.01,
        "Historical transaction profit; excludes customer acquisition "
        "and servicing costs.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.06, 1, 1])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
