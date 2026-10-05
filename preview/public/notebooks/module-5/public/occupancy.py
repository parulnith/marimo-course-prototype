# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.23.16",
#     "pandas>=2.2",
#     "pyodide-http; sys_platform == 'emscripten'",
# ]
# ///

# Adapted from marimo-studio examples/occupancy.py (Apache-2.0).
# Copyright 2026 Marimo. See licenses/marimo-studio-LICENSE.txt.
# Course changes: pandas implementation, bundled data, reusable functions, and
# command-line arguments. This is a score, not a fitted ML model.

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", app_title="Review room occupancy")

with app.setup:
    import argparse
    import sys

    import marimo as mo
    import pandas as pd


@app.function
def score_readings(readings):
    """Apply the official example's light/CO2 score to these readings."""
    if readings.empty:
        raise ValueError("Provide at least one sensor reading.")
    light_max = float(readings["Light"].quantile(0.99, interpolation="nearest"))
    co2_min = float(readings["CO2"].min())
    co2_max = float(readings["CO2"].quantile(0.99, interpolation="nearest"))
    scored = readings.copy()
    light_score = scored["Light"].clip(0, light_max) / max(light_max, 1.0)
    co2_score = (scored["CO2"].clip(co2_min, co2_max) - co2_min) / max(
        co2_max - co2_min, 1.0
    )
    scored["score"] = (0.7 * light_score + 0.3 * co2_score).astype("float32")
    return scored


@app.function
def evaluate_occupancy(scored, threshold=0.5):
    """Return per-row predictions and metrics for one decision threshold."""
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")
    if scored.empty:
        raise ValueError("Provide at least one scored reading.")
    rows = scored.copy()
    rows["predicted"] = (rows["score"] >= threshold).astype(int)
    actual = rows["Occupancy"] == 1
    predicted = rows["predicted"] == 1
    rows["outcome"] = "true negative"
    rows.loc[actual & predicted, "outcome"] = "true positive"
    rows.loc[~actual & predicted, "outcome"] = "false positive"
    rows.loc[actual & ~predicted, "outcome"] = "false negative"
    tp = int((actual & predicted).sum())
    tn = int((~actual & ~predicted).sum())
    fp = int((~actual & predicted).sum())
    fn = int((actual & ~predicted).sum())
    summary = {
        "threshold": threshold,
        "observations": len(rows),
        "accuracy": (tp + tn) / len(rows),
        "precision": tp / max(tp + fp, 1),
        "recall": tp / max(tp + fn, 1),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }
    return rows, summary


@app.cell
def script_options():
    # When the file runs in a terminal, read its optional command-line arguments.
    # In the notebook editor, keep using the interactive controls below.
    is_script = mo.app_meta().mode == "script"
    if is_script:
        parser = argparse.ArgumentParser(description="Evaluate room occupancy")
        parser.add_argument("--input", default="public/occupancy.csv")
        parser.add_argument("--threshold", type=float, default=0.5)
        parser.add_argument("--output", default="occupancy_predictions.csv")
        args = parser.parse_args()
    else:
        args = None
    return args, is_script


@app.cell(hide_code=True)
def introduction():
    mo.md("""
    # Review room occupancy

    Use light and CO₂ readings to estimate whether a room is occupied.
    Move the threshold to see how false positives and false negatives change.

    This course adaptation uses the scoring rule from
    [marimo-studio's occupancy example](https://marimo-team.github.io/marimo-studio/examples/occupancy?view=model-review).
    It combines normalized light (70%) and CO₂ (30%). It is not a trained model
    or a calibrated probability. Metrics describe these same observations,
    not performance on unseen data.
    """)
    return


@app.cell
def load_readings(args, is_script):
    if sys.platform == "emscripten":
        import pyodide_http
        pyodide_http.patch_all()
    data_source = (
        args.input
        if is_script
        else str(mo.notebook_location() / "public" / "occupancy.csv")
    )
    readings = pd.read_csv(data_source, parse_dates=["date"]).sort_values("date")
    readings.head(8)
    return (readings,)


@app.cell
def score_observations(readings):
    scored = score_readings(readings)
    return (scored,)


@app.cell
def threshold_control():
    threshold = mo.ui.slider(
        start=0.1, stop=0.9, step=0.05, value=0.5,
        label="Occupancy threshold", show_value=True,
    )
    threshold
    return (threshold,)


@app.cell
def selected_model(args, is_script, scored, threshold):
    selected_threshold = args.threshold if is_script else threshold.value
    prediction_rows, model_summary = evaluate_occupancy(scored, selected_threshold)
    error_rows = prediction_rows[
        prediction_rows["predicted"] != prediction_rows["Occupancy"]
    ]
    return error_rows, model_summary, prediction_rows


@app.cell(hide_code=True)
def metrics_output(model_summary):
    mo.hstack([
        mo.stat(label="Precision", value=f"{model_summary['precision']:.1%}"),
        mo.stat(label="Recall", value=f"{model_summary['recall']:.1%}"),
        mo.stat(label="False positives", value=str(model_summary["false_positive"])),
        mo.stat(label="False negatives", value=str(model_summary["false_negative"])),
    ], widths="equal")
    return


@app.cell(hide_code=True)
def prediction_table(prediction_rows):
    mo.vstack([
        mo.md("## Predictions beside observed occupancy"),
        mo.ui.table(prediction_rows, page_size=8),
    ])
    return


@app.cell(hide_code=True)
def errors_output(error_rows):
    mo.vstack([
        mo.md("## Inspect the errors\nA false positive predicts an occupied room when it was empty. A false negative misses an occupied room."),
        mo.ui.table(error_rows, page_size=8),
    ])
    return


@app.cell(hide_code=True)
def data_credit():
    mo.md("""
    Data: Luis Candanedo, [UCI Occupancy Detection](https://doi.org/10.24432/C5X01N),
    licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
    The bundled CSV contains 8,143 observations from the training split.
    """)
    return


@app.cell
def save_predictions(args, is_script, model_summary, prediction_rows):
    # In script mode, write the predictions and a short summary to the terminal.
    # The editor continues to show the results above without writing a file.
    if is_script:
        prediction_rows.to_csv(args.output, index=False)
        print(f"Wrote {len(prediction_rows)} rows to {args.output}")
        print(
            f"False positives: {model_summary['false_positive']}; "
            f"false negatives: {model_summary['false_negative']}"
        )
    return


if __name__ == "__main__":
    app.run()
