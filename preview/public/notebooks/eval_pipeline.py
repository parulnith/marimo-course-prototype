# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas", "altair"]
# ///

"""Reuse the notebook's helpers from another marimo notebook.
"""

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Reuse the classifier in another notebook

    This notebook imports `compare_reviews()` from the sentiment classifier
    notebook. You can now use it with a new set of reviews without copying the
    classification code.

    Make sure Ollama is running and that `gemma3:1b` and `qwen3:1.7b` are
    installed before you run the cells.
    """)
    return


@app.cell
def _():
    import marimo as mo

    from sentiment_classifier import compare_reviews

    return compare_reviews, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The import works like a normal Python import. Add the reviews you want to
    evaluate in the next cell.
    """)
    return


@app.cell
def _():
    texts = [
        "The new model is significantly faster and more accurate.",
        "Latency increased after the update. Very disappointed.",
        "Works about the same as before. No complaints.",
    ]
    return (texts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    `texts` contains three reviews that were not used in the first notebook.
    The next cell passes them to the imported comparison function.
    """)
    return


@app.cell
def _(compare_reviews, texts):
    results = compare_reviews(
        texts,
        "gemma3:1b",
        "qwen3:1.7b",
    )
    results
    return (results,)


@app.cell
def _(mo, results):
    _errors = (results["label"] == "error").sum()
    _avg_conf = results.loc[results["label"] != "error", "confidence"].mean()
    print(f"\nTotal rows : {len(results)}")
    print(f"Errors     : {_errors}")
    print(f"Avg conf   : {_avg_conf:.0%}")
    mo.hstack(
        [
            mo.stat(value=str(len(results)), label="Total rows"),
            mo.stat(value=str(_errors), label="Errors"),
            mo.stat(value=f"{_avg_conf:.0%}", label="Avg confidence"),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
