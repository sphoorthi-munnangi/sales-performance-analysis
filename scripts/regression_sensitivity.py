"""Check sensitivity of Furnishings regression to extreme margins."""

from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "Data" / "sample_-_superstore.xlsx"

FORMULA = (
    "profit_margin_pct ~ discount_pct "
    "+ C(Region) + C(Q('Product ID'))"
)


def fit_model(data):
    """Fit OLS with heteroskedasticity-robust standard errors."""
    return smf.ols(FORMULA, data=data).fit(cov_type="HC3")


def summarize(label, model):
    """Print comparable model statistics."""
    coefficient = model.params["discount_pct"]
    interval = model.conf_int().loc["discount_pct"]

    print(f"\n{label}")
    print("-" * 45)
    print(f"Observations: {int(model.nobs):,}")
    print(f"Discount coefficient: {coefficient:.4f}")
    print(
        "95% confidence interval: "
        f"[{interval.iloc[0]:.4f}, {interval.iloc[1]:.4f}]"
    )
    print(f"R-squared: {model.rsquared:.4f}")


def main():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")

    data = orders.loc[
        (orders["Sub-Category"] == "Furnishings")
        & (orders["Sales"] > 0)
    ].copy()

    data["profit_margin_pct"] = (
        data["Profit"] / data["Sales"] * 100
    )
    data["discount_pct"] = data["Discount"] * 100

    full_model = fit_model(data)

    reduced_data = data.loc[
        data["profit_margin_pct"] >= -100
    ].copy()

    reduced_model = fit_model(reduced_data)

    summarize("FULL DATASET", full_model)
    summarize("EXCLUDING MARGINS BELOW -100%", reduced_model)

    print(
        "\nExcluded observations:",
        len(data) - len(reduced_data)
    )
    print(
        "Note: This is a diagnostic comparison, "
        "not a recommendation to delete observations."
    )


if __name__ == "__main__":
    main()
