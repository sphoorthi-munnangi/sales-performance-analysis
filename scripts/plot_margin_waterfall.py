"""Create a waterfall chart of the 2025–2026 profit margin change."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "margin_decomposition.csv"
OUTPUT_FILE = ROOT / "outputs" / "margin_waterfall.png"

START_MARGIN = 13.465
NAVY = "#14263d"
TEAL = "#0f766e"
RED = "#b45353"

def main():
    data = pd.read_csv(INPUT_FILE)

    within = data["within_effect_pp"].sum()
    mix = data["sales_mix_effect_pp"].sum()
    end_margin = START_MARGIN + within + mix

    values = [START_MARGIN, within, mix, end_margin]
    labels = [
        "2025 margin",
        "Within-category\nchanges",
        "Sales-mix\nchanges",
        "2026 margin",
    ]

    bottoms = [
        0,
        min(START_MARGIN, START_MARGIN + within),
        min(START_MARGIN + within, end_margin),
        0,
    ]

    heights = [
        START_MARGIN,
        abs(within),
        abs(mix),
        end_margin,
    ]

    colors = [NAVY, RED, TEAL, NAVY]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        range(4),
        heights,
        bottom=bottoms,
        color=colors,
        width=0.6,
    )

    # Connector lines show how each change affects the running total.
    levels = [
        START_MARGIN,
        START_MARGIN + within,
        end_margin,
    ]

    for i, level in enumerate(levels):
        ax.plot(
            [i + 0.3, i + 0.7],
            [level, level],
            color="#999999",
            linestyle="--",
            linewidth=1,
        )

    for i, (value, bottom, height) in enumerate(
        zip(values, bottoms, heights)
    ):
        label = (
            f"{value:.3f}%"
            if i in (0, 3)
            else f"{value:+.3f} pp"
        )

        ax.text(
            i,
            bottom + height + 0.12,
            label,
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
        )

    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 15.5)
    ax.set_ylabel("Profit margin (%)")
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value:.0f}%")
    )

    ax.set_title(
        "What Changed the Profit Margin in 2026?",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=22,
    )

    ax.grid(axis="y", alpha=0.15)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(
        0.5,
        0.02,
        "Symmetric accounting decomposition; "
        "effects are measured in percentage points.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.05, 1, 1])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")
    print(f"2025 margin: {START_MARGIN:.3f}%")
    print(f"Within-category effect: {within:+.3f} pp")
    print(f"Sales-mix effect: {mix:+.3f} pp")
    print(f"2026 margin: {end_margin:.3f}%")


if __name__ == "__main__":
    main()
