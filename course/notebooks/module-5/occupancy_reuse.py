# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.23.16",
#     "pandas>=2.2",
#     "requests",
#     "pyodide-http; sys_platform == 'emscripten'",
# ]
# ///
import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import sys as _sys
    if _sys.platform == "emscripten":
        from pathlib import Path as _Path
        import marimo as _mo
        import pyodide_http as _pyodide_http
        import requests as _requests
        _pyodide_http.patch_all()
        _response = _requests.get(str(_mo.notebook_location() / "public" / "occupancy.py"))
        _response.raise_for_status()
        _directory = _Path("/tmp/occupancy_course")
        _directory.mkdir(exist_ok=True)
        (_directory / "occupancy.py").write_text(_response.text)
        _sys.path.insert(0, str(_directory))
    _module_ready = True
    return (_module_ready,)


@app.cell
def _(_module_ready):
    import marimo as mo
    import pandas as pd
    from occupancy import evaluate_occupancy, score_readings
    return evaluate_occupancy, mo, pd, score_readings


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Compare decision thresholds

    Import functions from `occupancy.py` and reuse them to compare three
    thresholds on the same sensor readings. Keep both notebooks in the same
    folder when working locally. The hidden browser setup cell makes that
    import available in this course's embedded notebook.
    """)
    return


@app.cell
def _(mo, pd, score_readings):
    readings = pd.read_csv(str(mo.notebook_location() / "public" / "occupancy.csv"))
    scored = score_readings(readings)
    return (scored,)


@app.cell
def _():
    thresholds = [0.3, 0.5, 0.7]
    return (thresholds,)


@app.cell
def _(evaluate_occupancy, pd, scored, thresholds):
    summaries = [evaluate_occupancy(scored, value)[1] for value in thresholds]
    comparison = pd.DataFrame(summaries)
    comparison
    return (comparison,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    A higher threshold predicts fewer occupied readings. Compare false positives
    and false negatives before choosing a threshold for a task. These metrics
    use the same observations that define the score's normalization.
    """)
    return


if __name__ == "__main__":
    app.run()
