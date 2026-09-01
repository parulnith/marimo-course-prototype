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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the dataset

    Let's load the Adult Income data from a CSV file with `pd.read_csv()`.

    - `na_values="?"` treats a question mark as a missing value.
    - `skipinitialspace=True` removes spaces that appear after commas in the CSV file.
    - The new `income` column uses `0` for income at or below $50K and `1` for income above $50K.
    - The final line removes the original text label and rows with missing values.
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
    ## Raw dataframe

    When a dataframe is the final expression in a cell, marimo displays it as an interactive table. You can page through rows, search for values, sort columns, and filter the data.

    `df[:1000]` returns the first 1,000 rows. This keeps the interactive view quick while giving you enough rows to inspect.
    """)
    return


@app.cell
def _(df):
    df[:1000]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            "`mo.plain()` turns off marimo's interactive dataframe viewer for one output. "
            "Here, `df.head()` returns the first five rows and `mo.plain()` displays them "
            "as a simple static preview."
        ),
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

    `mo.ui.data_editor()` creates an editable table. Here, `df.head(20)` gives the editor the first 20 rows. Use the editor for small experiments where you want to change a value and inspect the result.

    The variable `data_editor` refers to the widget. Writing it as the final expression displays the widget in the notebook.
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
    Every marimo UI element has a `.value`. For a data editor, `.value` is the dataframe with the current edits. When you change a value in the editor, marimo updates `edited_df` and reruns cells that use it.
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
    The `editable_columns` argument controls which columns a learner can change. In this example, `age` and `education` are editable. The other columns remain visible but cannot be changed.
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

    `mo.ui.table()` creates an interactive table for selecting rows without changing their values. Here, `df.head(100)` supplies the first 100 rows. The `selection="multi"` option lets you select more than one row.
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
    For a table, `.value` is a dataframe containing the selected rows. When you change the selection, marimo updates `selected_rows` and reruns cells that use it.
    """)
    return


@app.cell
def _(table):
    selected_rows = table.value
    selected_rows
    return


if __name__ == "__main__":
    app.run()
