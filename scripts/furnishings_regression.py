"""Exploratory regression of Furnishings profitability on discounts."""

from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"
OUTPUT_FILE = ROOT / "outputs" / "furnishings_regression.txt"


def main():
    data = pd.read_excel(DATA_FILE, sheet_name="Orders")

    furnishings = data.loc[
        data["Sub-Category"] == "Furnishings"
    ].copy()

    furnishings = furnishings.loc[
        furnishings["Sales"] > 0
    ].copy()

    furnishings["profit_margin_pct"] = (
        furnishings["Profit"] / furnishings["Sales"] * 100
    )

    furnishings["discount_pct"] = (
        furnishings["Discount"] * 100
    )

    # Product fixed effects compare transactions involving the same
    # products; region fixed effects account for regional differences.
    model = smf.ols(
        formula=(
            "profit_margin_pct ~ discount_pct "
            "+ C(Region) + C(Q('Product ID'))"
        ),
        data=furnishings,
    ).fit(cov_type="HC3")

    coefficient = model.params["discount_pct"]
    p_value = model.pvalues["discount_pct"]
    confidence_interval = model.conf_int().loc["discount_pct"]

    report = [
        "FURNISHINGS PROFITABILITY REGRESSION",
        "=" * 50,
        f"Observations: {int(model.nobs):,}",
        f"Products: {furnishings['Product ID'].nunique():,}",
        f"R-squared: {model.rsquared:.4f}",
        "",
        "DISCOUNT COEFFICIENT",
        f"Estimate: {coefficient:.4f}",
        f"95% confidence interval: "
        f"[{confidence_interval.iloc[0]:.4f}, "
        f"{confidence_interval.iloc[1]:.4f}]",
        f"P-value: {p_value:.6g}",
        "",
        "INTERPRETATION",
        "The coefficient estimates the association between a",
        "one-percentage-point increase in discount and the",
        "transaction profit margin in percentage points,",
        "holding product and region indicators constant.",
        "",
        "LIMITATIONS",
        "This is an observational, exploratory model.",
        "It does not establish causation.",
        "HC3 standard errors address heteroskedasticity,",
        "but not dependence among transactions.",
        "Transaction-level margins are not sales-weighted.",
        "Model diagnostics and sensitivity checks are needed.",
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    print("\n".join(report))
    print(f"\nReport saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
