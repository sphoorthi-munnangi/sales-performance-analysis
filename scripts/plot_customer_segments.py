"""Compare customer share and historical revenue share by RFM segment."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "outputs" / "customer_segments_summary.csv"
OUTPUT_FILE = ROOT / "outputs" / "customer_segments.png"

NAVY = "#14263d"
TEAL = "#0f766e"

SEGMENT_ORDER = [
    "Champions",
    "Loyal customers",
    "Potential loyalists",
    "At-risk high-value",
    "Other customers",
]


def main():
    data = pd.read_csv(INPUT_FILE, index_col="segment")

    missing = set(SEGMENT_ORDER) - set(data.index)
    if missing:
        raise ValueError(f"Missing customer segments: {sorted(missing)}")

    data = data.loc[SEGMENT_ORDER]

    customer_share = data["customer_share_pct"].to_numpy()
    revenue_share = data["revenue_share_pct"].to_numpy()

    y = np.arange(len(data))
    bar_height = 0.34

    fig, ax = plt.subplots(figsize=(11, 6.5))

    customer_bars = ax.barh(
        y - bar_height / 2,
        customer_share,
        height=bar_height,
        color=NAVY,
        label="Share of customers",
    )

    revenue_bars = ax.barh(
        y + bar_height / 2,
        revenue_share,
        height=bar_height,
        color=TEAL,
        label="Share of revenue",
    )

    for bars in [customer_bars, revenue_bars]:
        for bar in bars:
            value = bar.get_width()
            ax.text(
                value + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.1f}%",
                va="center",
                fontsize=10,
                color=NAVY,
            )

    ax.set_yticks(y)
    ax.set_yticklabels(SEGMENT_ORDER)
    ax.invert_yaxis()

    ax.set_xlim(0, 52)
    ax.set_xlabel("Share (%)")
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value:.0f}%")
    )

    ax.set_title(
        "Customer Segments: Population vs. Revenue",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=20,
    )

    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    fig.text(
        0.5,
        0.02,
        "RFM segments are rule-based and descriptive. "
        "Revenue represents historical sales, not future value.",
        ha="center",
        fontsize=9,
        color="#666666",
    )

    fig.tight_layout(rect=[0, 0.05, 1, 1])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
