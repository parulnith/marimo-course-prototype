# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.15.0",
#     "matplotlib>=3.8.0",
#     "pandas>=2.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Reactive compound interest

    Change `years` from `20` to `50` in the parameters cell. marimo will
    update the balance, table, chart, and summary because each output
    depends on the same inputs.
    """)
    return


@app.cell
def _():
    # Learner action: change years from 20 to 50 and run this cell.
    principal = 10_000
    annual_rate = 0.05
    years = 20
    return annual_rate, principal, years


@app.cell
def _(annual_rate, principal, years):
    yearly_records = [
        {
            "year": year,
            "balance": principal * (1 + annual_rate) ** year,
        }
        for year in range(years + 1)
    ]
    final_balance = yearly_records[-1]["balance"]
    return final_balance, yearly_records


@app.cell
def _(pd, yearly_records):
    yearly_table = pd.DataFrame(yearly_records)
    yearly_table["balance"] = yearly_table["balance"].round(2)
    yearly_table
    return (yearly_table,)


@app.cell
def _(plt, yearly_table):
    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.plot(yearly_table["year"], yearly_table["balance"], color="#2e7d5b", linewidth=2.5)
    axis.set(title="Compound growth", xlabel="Year", ylabel="Balance")
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure
    return


@app.cell
def _(annual_rate, final_balance, mo, principal, years):
    summary = (
        f"An initial balance of ${principal:,.0f} growing at "
        f"{annual_rate:.1%} per year is worth ${final_balance:,.2f} "
        f"after {years} years."
    )
    mo.callout(summary, kind="success")
    return


if __name__ == "__main__":
    app.run()
