# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "pandas"]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Sentiment classifier report

    This report uses results from the same product-review classifier. Run the classifier script first,
    then use this notebook to inspect and export the saved CSV file.
    """)
    return


@app.cell
def _(mo):
    path = mo.ui.text(value="results.csv", label="Results CSV")
    load = mo.ui.run_button(label="Load report", kind="success")
    mo.hstack([path, load], justify="start")
    return load, path


@app.cell
def _(load, mo, path, pd):
    mo.stop(not load.value, mo.md("Run the script, then select **Load report**."))
    results = pd.read_csv(path.value)
    results
    return (results,)


@app.cell
def _(mo, results):
    summary = results.groupby(["model", "label"], as_index=False).size().rename(columns={"size": "reviews"})
    mo.vstack([mo.md("## Label counts"), summary])
    return


if __name__ == "__main__":
    app.run()
