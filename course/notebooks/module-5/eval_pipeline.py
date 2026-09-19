# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas", "altair"]
# ///

"""Reuse the notebook's helpers from a marimo notebook OR a plain script.
"""

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-for-ai-and-ml-development-oreilly-workshop/blob/main/Module_5/eval_pipeline.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Eval Pipeline (notebook)

    A marimo notebook that imports `compare_two_models` and `get_client` from
    `sentiment_classifier.py` and runs them on three reviews.
    """)
    return


@app.cell
def _():
    import marimo as mo

    from sentiment_classifier import compare_two_models, get_client

    return compare_two_models, get_client, mo


@app.cell
def _(get_client):
    client = get_client()
    return (client,)


@app.cell
def _():
    texts = [
        "The new model is significantly faster and more accurate.",
        "Latency increased after the update. Very disappointed.",
        "Works about the same as before. No complaints.",
    ]
    return (texts,)


@app.cell
def _(client, compare_two_models, texts):
    results = compare_two_models(client, texts, model_a="gemma3:1b", model_b="qwen2.5:0.5b")
    # print(results[["model", "text", "label", "confidence"]].to_string(index=False))
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
