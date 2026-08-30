# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.23.16",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Inspect and edit data

    Let's load the dataset and create a dataframe named `df`. The code converts the original income label into `0` for income at or below $50K and `1` for income above $50K.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


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
    ## Raw dataframe

    The dataframe output gives you a first view of the dataset. marimo lets you page through rows, search for values, sort columns, and filter the data.
    """)
    return


@app.cell
def _(df):
    df[:1000]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md("To display a dataframe without the interactive viewer, use `mo.plain()`."),
        kind="info",
    )
    return


@app.cell
def _(df, mo):
    mo.plain(df.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data editor

    `mo.ui.data_editor()` makes a dataframe editable. Use it for small experiments where you want to change a few values and inspect the result.
    """)
    return


@app.cell
def _(df, mo):
    data_editor = mo.ui.data_editor(data=df.head(20))
    data_editor
    return (data_editor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The edited dataframe is available through `.value`.
    """)
    return


@app.cell
def _(data_editor):
    edited_df = data_editor.value
    edited_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's restrict editing to the `age` and `education` columns.
    """)
    return


@app.cell
def _(df, mo):
    mo.ui.data_editor(
        data=df.head(20),
        editable_columns=["age", "education"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Select rows with a table

    Let's use `mo.ui.table()` to select rows without changing their values. The `selection="multi"` option lets you select more than one row.
    """)
    return


@app.cell
def _(df, mo):
    table = mo.ui.table(data=df.head(100), selection="multi")
    table
    return (table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The selected rows are available through `.value`.
    """)
    return


@app.cell
def _(table):
    selected_rows = table.value
    selected_rows
    return


if __name__ == "__main__":
    app.run()
