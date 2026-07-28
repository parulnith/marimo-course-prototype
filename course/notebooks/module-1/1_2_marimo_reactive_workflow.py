# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.22.4",
#     "matplotlib==3.10.8",
#     "pandas==3.0.1",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop/blob/main/Module_1/1_2_marimo_reactive_workflow.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Same Workflow, Reactively with marimo


    We start with the same **plain compound-interest workflow** from Section 1.2:
    fixed parameters, a helper function, a computed result, a plot, a table.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import time

    return mo, pd, plt, time


@app.function
def compound_interest(principal, rate, years):
    values = [principal]
    for _year in range(1, years + 1):
        values.append(values[-1] * (1 + rate))
    return values


@app.cell
def _():
    principal = 1000
    rate = 0.07
    years = 20
    growth = compound_interest(principal, rate, years)
    return growth, principal, rate, years


@app.cell(hide_code=True)
def _(growth, mo, rate, years):
    mo.md(f"""
    After **{years} years** at **{rate:.0%}**, the account grows to
    **${growth[-1]:,.2f}**.
    """)
    return


@app.cell
def _(time):
    time.sleep(5)
    return


@app.cell
def _(growth, plt, years):
    _, ax = plt.subplots()
    ax.plot(range(years + 1), growth, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Balance ($)")
    ax.set_title(f"Compound Interest Growth ({years} years)")
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare multiple interest rates

    Same idea as before, but the table stays aligned automatically with the current inputs.
    """)
    return


@app.cell
def _():
    rates = [0.03, 0.05, 0.07, 0.10]
    return (rates,)


@app.cell
def _(mo, pd, principal, rates, years):
    rows = []
    for comparison_rate in rates:
        scenario_growth = compound_interest(principal, comparison_rate, years)
        rows.append(
            {
                "rate": f"{comparison_rate:.0%}",
                "years_used": years,
                "final_value": scenario_growth[-1],
            }
        )
    summary_df = pd.DataFrame(rows)
    mo.plain(summary_df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### Coming from Jupyter?

    You don't have to start from scratch. Convert any `.ipynb` to a marimo notebook with one command:

    ```bash
    marimo convert notebook.ipynb -o notebook.py
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
