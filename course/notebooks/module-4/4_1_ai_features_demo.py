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
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # AI features and agent context

    This notebook contains a small sales dataset and two interactive
    controls. Use it to practise adding variables to AI prompts and pairing
    a coding agent with a running marimo notebook.
    """)
    return


@app.cell
def _(pd):
    df = pd.DataFrame(
        {
            "region": [
                "North", "North", "South", "South", "East",
                "East", "West", "West", "Central", "Central",
            ],
            "segment": [
                "Enterprise", "SMB", "Enterprise", "SMB", "Midmarket",
                "SMB", "Enterprise", "Midmarket", "SMB", "Midmarket",
            ],
            "channel": [
                "Direct", "Partner", "Direct", "Online", "Partner",
                "Online", "Direct", "Partner", "Online", "Direct",
            ],
            "revenue": [82000, 38000, 76000, 29000, 54000, 24000, 91000, 61000, 31000, 59000],
            "cost": [42000, 21000, 39000, 18000, 31000, 15000, 47000, 33000, 19000, 32000],
            "satisfaction": [8.7, 7.8, 8.1, 6.9, 7.4, 6.5, 9.0, 8.0, 7.1, 7.9],
            "converted": [True, True, True, False, True, False, True, True, False, True],
        }
    )
    df["profit"] = df["revenue"] - df["cost"]
    df["margin"] = df["profit"] / df["revenue"]
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Inspect the data

    The dataframe is named `df`. Add `@df` to a prompt when the assistant
    needs information about its columns and data types.
    """)
    return


@app.cell
def _(df):
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Select what to compare

    The next cell creates two controls. Their current choices are available
    through `metric_selector.value` and `segment_selector.value`.
    """)
    return


@app.cell
def _(df, mo):
    metric_selector = mo.ui.dropdown(
        options=["revenue", "cost", "profit", "margin", "satisfaction"],
        value="revenue",
        label="Metric",
    )
    segment_selector = mo.ui.multiselect(
        options=sorted(df["segment"].unique()),
        value=sorted(df["segment"].unique()),
        label="Segments",
    )
    mo.vstack([metric_selector, segment_selector])
    return metric_selector, segment_selector


@app.cell
def _(df, metric_selector, segment_selector):
    selected_segments = segment_selector.value
    selected_metric = metric_selector.value
    filtered_df = df[df["segment"].isin(selected_segments)].copy()
    metric_summary = (
        filtered_df.groupby("segment", as_index=False)[selected_metric]
        .mean()
        .sort_values(selected_metric, ascending=False)
    )
    metric_summary
    return metric_summary, selected_metric


@app.cell
def _(metric_summary, plt, selected_metric):
    fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
    ax.bar(
        metric_summary["segment"],
        metric_summary[selected_metric],
        color="#4C72B0",
    )
    ax.set_title(f"Average {selected_metric} by segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel(selected_metric)
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Work with an assistant or coding agent

    Try a focused request in marimo's built in assistant:

    ```text
    Using @df, add a cell that computes total revenue and profit by channel.
    ```

    For a larger task, pair a coding agent with this notebook. Ask it to add
    a low margin analysis that depends on the current segment selection.
    Review every new cell and output before keeping the changes.
    """)
    return


if __name__ == "__main__":
    app.run()
