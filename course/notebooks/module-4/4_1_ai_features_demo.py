# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.20.4",
#     "matplotlib>=3.9.0",
#     "pandas>=2.2.0",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## AI-assisted sales analysis
    """)
    return


if __name__ == "__main__":
    app.run()
