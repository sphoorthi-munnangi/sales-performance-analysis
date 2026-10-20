"""Visualize monthly sales and profitability across four years."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "monthly_performance.png"

NAVY = "#14263d"
TEAL = "#0f766e"
RED = "#b45353"


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")
    orders["Order Date"] = pd.to_datetime(orders["Order Date"])
    orders["Month"] = orders["Order Date"].dt.month

    monthly = (
        orders.groupby("Month")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
        )
        .reindex(range(1, 13))
    )

    monthly["margin_pct"] = (
        monthly["profit"] / monthly["sales"] * 100
    )

    overall_margin = (
        orders["Profit"].sum() / orders["Sales"].sum() * 100
    )

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    x = np.arange(12)

    fig, axes = plt.subplots(
        2, 1,
        figsize=(12, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 1]},
    )

    # Panel 1: Sales
    axes[0].bar(
        x,
        monthly["sales"],
        color=TEAL,
        width=0.7,
    )

    axes[0].set_title(
        "Monthly Sales",
        fontsize=14,
        color=NAVY,
        fontweight="bold",
        loc="left",
    )

    axes[0].set_ylabel("Total sales ($)")
    axes[0].yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"${value / 1000:,.0f}k")
    )

    # Panel 2: Profit margin
    margins = monthly["margin_pct"].to_numpy()

    colors = [
        TEAL if margin >= overall_margin else RED
        for margin in margins
    ]

    axes[1].bar(
        x,
        margins,
        color=colors,
        width=0.7,
    )

    axes[1].axhline(
        overall_margin,
        color=NAVY,
        linestyle="--",
        linewidth=1.5,
        label=f"Overall margin: {overall_margin:.2f}%",
    )

    axes[1].set_title(
        "Monthly Profit Margin",
        fontsize=14,
        color=NAVY,
        fontweight="bold",
        loc="left",
    )

    axes[1].set_ylabel("Profit margin (%)")
    axes[1].legend(frameon=False, loc="upper right")

    axes[1].set_xticks(x)
    axes[1].set_xticklabels(months)
    axes[1].set_xlabel("Calendar month")

    for ax in axes:
        ax.grid(axis="y", alpha=0.15)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle(
        "Retail Sales and Profitability by Month",
        fontsize=18,
        fontweight="bold",
        color=NAVY,
        y=0.98,
    )

    fig.text(
        0.5,
        0.015,
        "Each month combines observations from 2023–2026. "
        "Margins are calculated as total profit / total sales.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.04, 1, 0.95])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")
    print(f"Overall profit margin: {overall_margin:.2f}%")


if __name__ == "__main__":
    main()
