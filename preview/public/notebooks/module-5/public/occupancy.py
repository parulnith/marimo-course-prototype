# /// script
# requires-python = ">=3.11,<3.15"
# dependencies = [
#     "marimo>=0.23.16",
#     "pandas>=2.2",
#     "pyodide-http; sys_platform == 'emscripten'",
#     "marimo-studio==0.2.3",
#     "altair==6.3.0"
# ]
#
# [tool.marimo-studio]
# default = "monitor"
#
# [tool.marimo-studio.cells]
# ///

# Adapted from marimo-studio examples/occupancy.py (Apache-2.0).
# Copyright 2026 Marimo. See licenses/marimo-studio-LICENSE.txt.
# Course changes: pandas implementation, bundled data, reusable functions, and
# command-line arguments. This is a score, not a fitted ML model.

import marimo

__generated_with = "0.25.0"
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
    return error_rows, model_summary, prediction_rows, selected_threshold


@app.cell(hide_code=True)
def threshold_sweep(scored):
    # Evaluate every slider position with the same function the notebook uses.
    sweep_thresholds = [round(0.1 + 0.05 * step, 2) for step in range(17)]
    threshold_sweep = pd.DataFrame(
        [evaluate_occupancy(scored, value)[1] for value in sweep_thresholds]
    )
    return (threshold_sweep,)


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
def tradeoff_output(selected_threshold, threshold_sweep):
    import altair as alt

    _marker = (
        alt.Chart(pd.DataFrame({"threshold": [selected_threshold]}))
        .mark_rule(color="gray", strokeDash=[4, 4])
        .encode(x="threshold:Q")
    )
    _errors = threshold_sweep.melt(
        id_vars="threshold",
        value_vars=["false_positive", "false_negative"],
        var_name="error",
        value_name="count",
    ).replace(
        {
            "false_positive": "False positives",
            "false_negative": "False negatives",
        }
    )
    _rates = threshold_sweep.melt(
        id_vars="threshold",
        value_vars=["precision", "recall"],
        var_name="metric",
        value_name="value",
    ).replace({"precision": "Precision", "recall": "Recall"})
    _error_chart = (
        alt.Chart(_errors, title="Errors by threshold")
        .mark_line(point=True)
        .encode(
            x=alt.X("threshold:Q", title="Threshold"),
            y=alt.Y("count:Q", title="Readings"),
            color=alt.Color("error:N", title=None),
            tooltip=["threshold", "error", "count"],
        )
    )
    _rate_chart = (
        alt.Chart(_rates, title="Precision and recall by threshold")
        .mark_line(point=True)
        .encode(
            x=alt.X("threshold:Q", title="Threshold"),
            y=alt.Y(
                "value:Q",
                title=None,
                axis=alt.Axis(format="%"),
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color("metric:N", title=None),
            tooltip=[
                "threshold",
                "metric",
                alt.Tooltip("value:Q", format=".1%"),
            ],
        )
    )
    tradeoff_chart = alt.hconcat(
        (_error_chart + _marker).properties(width=320, height=220),
        (_rate_chart + _marker).properties(width=320, height=220),
    ).resolve_scale(color="independent")
    tradeoff_chart
    return (alt,)


@app.cell(hide_code=True)
def confusion_output(model_summary):
    confusion_matrix = pd.DataFrame(
        {
            "Predicted empty": [
                model_summary["true_negative"],
                model_summary["false_negative"],
            ],
            "Predicted occupied": [
                model_summary["false_positive"],
                model_summary["true_positive"],
            ],
        },
        index=pd.Index(
            ["Actually empty", "Actually occupied"], name="Recorded"
        ),
    )
    confusion_matrix
    return


@app.cell(hide_code=True)
def score_distribution_output(alt, prediction_rows, selected_threshold):
    # Bin scores here so the chart receives counts, not all 8,143 rows.
    _bins = pd.interval_range(0, 1, freq=0.025)
    score_bins = (
        prediction_rows.assign(
            bin=pd.cut(prediction_rows["score"], _bins, include_lowest=True),
            recorded=prediction_rows["Occupancy"].map(
                {0: "Empty", 1: "Occupied"}
            ),
        )
        .groupby(["bin", "recorded"], observed=False)
        .size()
        .reset_index(name="readings")
        .assign(
            start=lambda f: f["bin"].map(lambda b: b.left),
            end=lambda f: f["bin"].map(lambda b: b.right),
        )
        .drop(columns="bin")
    )
    score_distribution = (
        alt.Chart(score_bins, title="Scores by recorded occupancy")
        .mark_bar(opacity=0.7)
        .encode(
            x=alt.X("start:Q", title="Score", bin="binned"),
            x2="end:Q",
            y=alt.Y("readings:Q", title="Readings", stack=None),
            color=alt.Color("recorded:N", title="Recorded"),
            tooltip=["start", "end", "recorded", "readings"],
        )
        + alt.Chart(pd.DataFrame({"threshold": [selected_threshold]}))
        .mark_rule(color="gray", strokeDash=[4, 4])
        .encode(x="threshold:Q")
    ).properties(width=680, height=220)
    score_distribution
    return


@app.cell(hide_code=True)
def report_summary_output(model_summary, selected_threshold):
    # Report text built from the current results, so the numbers always match.
    _s = model_summary

    def _count(n, word):
        return f"{n:,} {word}" + ("" if n == 1 else "s")

    report_summary = mo.md(f"""
    At a threshold of **{selected_threshold:.2f}**, the rule predicted that
    {_s["true_positive"] + _s["false_positive"]:,} of {_s["observations"]:,} readings
    came from an occupied room.

    - **Precision {_s["precision"]:.1%}:** of the readings predicted as occupied, this share really were.
    - **Recall {_s["recall"]:.1%}:** of the readings from occupied rooms, this share were caught.
    - **{_count(_s["false_positive"], "false positive")}:** empty rooms treated as occupied, which can waste energy.
    - **{_count(_s["false_negative"], "false negative")}:** occupied rooms treated as empty, which can switch lights off on people.
    """)
    report_summary
    return


@app.cell(hide_code=True)
def report_headline_output(model_summary, selected_threshold, threshold_sweep):
    # Key finding for the report, from the threshold sweep.
    _s = model_summary
    _t = round(selected_threshold, 2)
    _errors = threshold_sweep.assign(
        total_errors=threshold_sweep["false_positive"]
        + threshold_sweep["false_negative"]
    )
    _best = _errors.loc[_errors["total_errors"].idxmin()]
    _current_total = _s["false_positive"] + _s["false_negative"]
    _best_line = (
        "This is also the threshold with the fewest total errors."
        if abs(_best["threshold"] - _t) < 1e-9
        else (
            f"The fewest total errors ({int(_best['total_errors']):,}) occur at "
            f"**{_best['threshold']:.2f}**, compared with {_current_total:,} at the current threshold."
        )
    )
    report_headline = mo.callout(
        mo.md(
            f"**Current threshold: {_t:.2f}.** It misclassifies {_current_total:,} of "
            f"{_s['observations']:,} readings ({_current_total / _s['observations']:.1%}). "
            + _best_line
        ),
        kind="info",
    )
    report_headline
    return


@app.cell(hide_code=True)
def threshold_comparison_output(selected_threshold, threshold_sweep):
    # Candidate thresholds for the report table, plus the current one.
    _current = round(selected_threshold, 2)
    _candidates = {0.4, 0.45, 0.5, 0.55, 0.6, 0.7, _current}
    _rows = threshold_sweep[
        threshold_sweep["threshold"].round(2).isin(_candidates)
    ]

    def _row_html(row):
        is_current = round(row.threshold, 2) == _current
        label = f"{row.threshold:.2f}" + (" (current)" if is_current else "")
        cells = [
            label,
            f"{row.precision:.1%}",
            f"{row.recall:.1%}",
            f"{int(row.false_positive):,}",
            f"{int(row.false_negative):,}",
            f"{int(row.false_positive + row.false_negative):,}",
        ]
        attrs = ' class="current"' if is_current else ""
        return (
            f"<tr{attrs}>"
            + "".join(f"<td>{cell}</td>" for cell in cells)
            + "</tr>"
        )

    _headers = [
        "Threshold",
        "Precision",
        "Recall",
        "False positives",
        "False negatives",
        "Total errors",
    ]
    threshold_comparison = mo.Html(
        '<table class="threshold-comparison"><thead><tr>'
        + "".join(f"<th>{h}</th>" for h in _headers)
        + "</tr></thead><tbody>"
        + "".join(_row_html(row) for row in _rows.itertuples())
        + "</tbody></table>"
    )
    threshold_comparison
    return


@app.cell(hide_code=True)
def report_error_table_output(error_rows):
    # A short, static error table for printed reports (the full table is in errors_output).
    _columns = {
        "date": "Time",
        "Light": "Light",
        "CO2": "CO₂",
        "score": "Score",
        "Occupancy": "Recorded",
        "predicted": "Predicted",
        "outcome": "Error type",
    }
    _labels = {0: "Empty", 1: "Occupied"}
    _sample = error_rows.head(10)

    def _cells(row):
        return [
            row["date"].strftime("%Y-%m-%d %H:%M"),
            f"{row['Light']:,.0f}",
            f"{row['CO2']:,.0f}",
            f"{row['score']:.2f}",
            _labels[int(row["Occupancy"])],
            _labels[int(row["predicted"])],
            row["outcome"].capitalize(),
        ]

    report_error_table = mo.vstack(
        [
            mo.Html(
                '<table class="report-errors"><thead><tr>'
                + "".join(f"<th>{label}</th>" for label in _columns.values())
                + "</tr></thead><tbody>"
                + "".join(
                    "<tr>"
                    + "".join(f"<td>{cell}</td>" for cell in _cells(row))
                    + "</tr>"
                    for _, row in _sample.iterrows()
                )
                + "</tbody></table>"
            ),
            mo.md(
                f"Showing {len(_sample):,} of {len(error_rows):,} prediction errors, in time order."
            ),
        ]
    )
    report_error_table
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
