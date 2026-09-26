# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///
import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("""
    # Active environment starter

    Add the import cell from the lesson below this cell.
    """)
    return


if __name__ == "__main__":
    app.run()
