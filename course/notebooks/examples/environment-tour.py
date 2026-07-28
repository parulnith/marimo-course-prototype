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
    # Guided environment tour

    Use the controls below. Then open marimo's variables panel and
    dependency graph to see how the inputs connect to each output.
    """)
    return


@app.cell
def _(mo):
    # Learner action: change each control and watch all dependent outputs update.
    principal_input = mo.ui.number(
        start=1_000,
        stop=100_000,
        step=1_000,
        value=10_000,
        label="Principal",
    )
    annual_rate_slider = mo.ui.slider(
        start=0.01,
        stop=0.15,
        step=0.005,
        value=0.05,
        label="Annual rate",
        show_value=True,
    )
    years_slider = mo.ui.slider(
        start=1,
        stop=50,
        step=1,
        value=20,
        label="Years",
        show_value=True,
    )
    mo.hstack(
        [principal_input, annual_rate_slider, years_slider],
        justify="space-around",
        wrap=True,
    )
    return annual_rate_slider, principal_input, years_slider


@app.cell
def _(annual_rate_slider, principal_input, years_slider):
    principal = principal_input.value
    annual_rate = annual_rate_slider.value
    years = years_slider.value
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
    axis.fill_between(yearly_table["year"], yearly_table["balance"], alpha=0.12, color="#2e7d5b")
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


@app.cell
def _(mo):
    mo.md("""
    ## Continue the tour

    Open the variables panel, dependency graph, logs, and command palette.
    Edit an upstream value and inspect each cell's execution state.
    """)
    return


if __name__ == "__main__":
    app.run()
