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

    This notebook includes the table tools from section 3.1. It adds tools for building charts and transforming the dataframe.
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
    ## Inspect and edit data
    """)
    return


@app.cell
def _(df):
    df[:1000]
    return


@app.cell
def _(df, mo):
    data_editor = mo.ui.data_editor(data=df.head(20))
    data_editor
    return (data_editor,)


@app.cell
def _(data_editor):
    edited_df = data_editor.value
    edited_df
    return


@app.cell
def _(df, mo):
    table = mo.ui.table(data=df.head(100), selection="multi")
    table
    return (table,)


@app.cell
def _(table):
    selected_rows = table.value
    selected_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data explorer

    Choose fields and visual properties to build a chart.
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
    ## Dataframe transformer

    Filter, sort, group, and transform the dataframe.
    """)
    return


@app.cell
def _(df, mo):
    dataframe = mo.ui.dataframe(df)
    dataframe
    return


if __name__ == "__main__":
    app.run()
