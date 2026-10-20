"""Visualize the factors behind the 2025–2026 profit margin change."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "margin_decomposition.csv"
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "margin_drivers.png"

NAVY = "#14263d"
TEAL = "#0f766e"
RED = "#b45353"


def main():
    decomposition = pd.read_csv(INPUT_FILE)

    within = decomposition["within_effect_pp"].sum()
    mix = decomposition["sales_mix_effect_pp"].sum()

    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")
    orders["Year"] = pd.to_datetime(orders["Order Date"]).dt.year

    yearly = (
        orders.loc[orders["Year"].isin([2025, 2026])]
        .groupby("Year")[["Sales", "Profit"]]
        .sum()
    )

    margins = yearly["Profit"] / yearly["Sales"] * 100

    start_margin = margins.loc[2025]
    end_margin = margins.loc[2026]

    if abs((within + mix) - (end_margin - start_margin)) > 1e-8:
        raise ValueError("Margin decomposition does not reconcile.")

    labels = [
        "Within-category margins",
        "Sales mix",
    ]
    values = [within, mix]
    colors = [RED, TEAL]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    bars = ax.barh(
        labels,
        values,
        color=colors,
        height=0.45,
    )

    ax.invert_yaxis()
    ax.axvline(0, color=NAVY, linewidth=1.2)

    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:+.3f} pp",
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(8 if value >= 0 else -8, 0),
            textcoords="offset points",
            ha="left" if value >= 0 else "right",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
        )

    ax.set_xlim(-1.5, 0.9)
    ax.set_xlabel("Contribution to margin change (percentage points)")
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value:+.1f}")
    )

    ax.set_title(
        "What Contributed to the 2026 Profit Margin Decline?",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=45,
    )

    ax.text(
        0.5,
        1.08,
        f"2025: {start_margin:.3f}%   →   "
        f"2026: {end_margin:.3f}%",
        transform=ax.transAxes,
        ha="center",
        fontsize=13,
        color=NAVY,
    )

    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    fig.text(
        0.5,
        0.02,
        "Symmetric accounting decomposition; "
        "not a causal analysis.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.07, 1, 0.95])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
