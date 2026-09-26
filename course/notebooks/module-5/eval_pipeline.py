# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "marimo",
#   "pandas",
#   "requests",
#   "pyodide-http; sys_platform == 'emscripten'",
# ]
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


@app.cell(hide_code=True)
def _():
    import sys as _sys

    if _sys.platform == "emscripten":
        from pathlib import Path as _Path

        import marimo as _mo
        import pyodide_http as _pyodide_http
        import requests as _requests

        _pyodide_http.patch_all()
        _module_url = _mo.notebook_location() / "public" / "sentiment_classifier.py"
        _module_dir = _Path("/tmp/marimo_course_modules")
        _module_dir.mkdir(exist_ok=True)
        _module_path = _module_dir / "sentiment_classifier.py"
        _response = _requests.get(str(_module_url), timeout=30)
        _response.raise_for_status()
        _module_path.write_text(_response.text)
        _sys.path.insert(0, str(_module_dir))

    _browser_module_ready = True
    return (_browser_module_ready,)


@app.cell
def _(_browser_module_ready):
    import marimo as mo

    from sentiment_classifier import compare_reviews

    return compare_reviews, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    When both notebooks are in the same folder on your computer, the visible
    import above is all you need. This course runs the notebook in a browser,
    so a hidden cell first makes the bundled classifier file available to the
    browser's Python environment.

    Add the reviews you want to evaluate in the next cell.
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
    _models = results["model"].nunique()
    print(f"\nTotal rows : {len(results)}")
    print(f"Errors     : {_errors}")
    print(f"Models     : {_models}")
    mo.hstack(
        [
            mo.stat(value=str(len(results)), label="Total rows"),
            mo.stat(value=str(_errors), label="Errors"),
            mo.stat(value=str(_models), label="Models"),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
