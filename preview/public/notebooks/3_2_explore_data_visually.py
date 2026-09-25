# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==6.0.0",
#     "marimo==0.23.16",
#     "pandas==2.3.3",
#     "pyarrow==24.0.0",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Explore data visually

    This notebook continues the workflow from the previous section. Let's begin with the same imports and Adult Income dataset. We will create `df` in the same way, then use two of marimo's built-in tools to look for patterns in the data.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the dataset

    The imports and data preparation below are the same as in the previous notebook. They are included again so that you can run this notebook on its own.

    The data cell reads the Adult Income data into a pandas dataframe named `df`. It also changes the income label into `0` for income at or below $50K and `1` for income above $50K.
    """)
    return


@app.cell
def _(pd):
    adult_csv_url = "https://www.openml.org/data/get_csv/1595261/phpMawTba"
    df = pd.read_csv(adult_csv_url, na_values="?", skipinitialspace=True)
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data explorer

    `mo.ui.data_explorer(df)` creates a visual interface for exploring the dataframe. It is chart-first, so you can choose fields and look at their distributions or relationships before deciding which features are worth modelling.

    The dataframe `df` is the input. We assign the tool to `data_explorer`, then place that variable on the last line so marimo displays it.

    Try changing the chart type and the fields shown in the chart. You can also add a filter and watch the chart update.
    """)
    return


@app.cell
def _(df, mo):
    data_explorer = mo.ui.data_explorer(df)
    data_explorer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Transform a dataframe

    In the previous notebook, placing `df` at the end of a cell displayed the raw dataframe for inspection. `mo.ui.dataframe(df)` serves a different purpose. It lets you build transformations through an interface, such as sorting or filtering the rows.

    We assign the tool to `dataframe`, then place that variable on the last line so marimo displays it.
    """)
    return


@app.cell
def _(df, mo):
    dataframe = mo.ui.dataframe(df)
    dataframe
    return (dataframe,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dataframe tool keeps the transformed result in its `.value`. The next cell assigns that result to `transformed_df`, which makes it available to other Python cells.

    Change a sort or filter in the dataframe above. marimo updates `transformed_df` automatically because the cell below depends on the dataframe control.
    """)
    return


@app.cell
def _(dataframe):
    transformed_df = dataframe.value
    transformed_df
    return


if __name__ == "__main__":
    app.run()
