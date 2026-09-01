# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair==6.0.0",
#     "marimo>=0.23.1",
#     "matplotlib==3.10.7",
#     "numpy",
#     "pandas==2.3.3",
#     "pyarrow==24.0.0",
#     "scikit-learn==1.8.0",
#     "tabicl",
#     "vegafusion==2.0.3",
#     "vl-convert-python==1.9.0.post1",
# ]
# ///

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-oreilly-workshop/blob/main/Module_3/3_1_interactive_ml_workflow.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Interactive ML Workflow

    This notebook uses the idea for an end-to-end AI workflow. It starts with data inspection, moves into visual exploration, connects those choices to model training, and then uses model errors as the next input for analysis. Here, we will see **data, controls, models, and plots** behave as one live
    system.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import fetch_openml
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestClassifier
    from tabicl import TabICLClassifier

    return (
        LabelEncoder,
        RandomForestClassifier,
        TabICLClassifier,
        fetch_openml,
        mo,
        np,
        plt,
        roc_auc_score,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data
    We'll walk through one end-to-end AI workflow on the **Adult Income** dataset — a classic tabular benchmark from the US Census where the task is to predict whether a person earns more than $50K per year. It's a binary classification problem with a mix of numeric (age, hours-per-week, capital gains) and categorical (occupation, education, marital status) features.

    Here's the path we'll take:

    1. **Look at the data** — first as a raw dataframe, then as an editable sample.
    2. **Explore it visually** — drag columns into a chart, then sort and filter a table.
    3. **Pick features and sample size** — using widgets that drive the rest of the pipeline.
    4. **Fit and compare two models** — TabICL and Random Forest, side by side.
    5. **Debug errors interactively** — move a threshold, inspect misclassified rows

    Each stage introduces a marimo widget.
    """)
    return


@app.cell
def _(fetch_openml):
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.copy()
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    feature_options = [col for col in df.columns if col != "income"]
    return df, feature_options


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Raw dataframe

    The dataframe output gives you a baseline view of the dataset. marimo lets you page through, search, sort, and filter dataframes, making it extremely easy to get a feel for your data.
    """)
    return


@app.cell
def _(df):
    df[:1000]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To opt out of the rich dataframe viewer, use mo.plain:
    """)
    return


@app.cell
def _(df, mo):
    mo.plain(df.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Data Editor

    `mo.ui.data_editor(df)` makes tabular data editable. This is useful for
    small what-if experiments: change a few values and watch the downstream
    summary update automatically.
    """)
    return


@app.cell
def _(df, mo):
    data_editor = mo.ui.data_editor(df)
    data_editor
    return (data_editor,)


@app.cell
def _(data_editor):
    data_editor.value
    return


@app.cell
def _(df, mo):
    mo.ui.data_editor(df, editable_columns=["age", "education"])
    return


@app.cell
def _(df, mo):
    editor = mo.ui.table(df)
    editor
    return (editor,)


@app.cell
def _(editor):
    editor.value
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Visualization

    After looking at the raw table and an editable sample, move into marimo's
    visual exploration tools. These help you go from rows and columns to
    patterns, distributions, and relationships.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Data Explorer

    `mo.ui.data_explorer(df)` is chart-first. Use it when you want to explore
    distributions and relationships visually before deciding which features
    are worth modelling.
    """)
    return


@app.cell
def _(df, mo):
    data_explorer = mo.ui.data_explorer(df)
    data_explorer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### DataFrame


    `mo.ui.dataframe(df)` is the interactive table view. Use it to sort
    columns, filter rows, and inspect subsets once you know what you want to
    look at more closely.
    """)
    return


@app.cell
def _(df, mo):
    mo.ui.dataframe(df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Modeling

    The goal here is to show how the same dataset and the same selected
    features can be pushed through multiple models inside one reactive
    notebook.

    We compare TabICL with Random Forest on the same train/test split and use
    ROC AUC plus probability plots to see how their behavior changes when the
    selected features change.
    """)
    return


@app.cell
def _(feature_options, mo):
    selected_features_ui = mo.ui.multiselect(
        options=feature_options,
        value=feature_options,
        label="Features to include in the model",
    )
    sample_size_ui = mo.ui.slider(
        start=500,
        stop=3000,
        step=500,
        value=1000,
        label="Rows to sample for modeling",
    )
    preview_rows = mo.ui.slider(
        start=5,
        stop=25,
        step=5,
        value=10,
        label="Rows to preview in the error table",
    )
    mo.vstack([selected_features_ui, sample_size_ui, preview_rows])
    return preview_rows, sample_size_ui, selected_features_ui


@app.cell
def _(
    LabelEncoder,
    df,
    sample_size_ui,
    selected_features_ui,
    train_test_split,
):
    selected_features = selected_features_ui.value
    sample_size = sample_size_ui.value
    sampled_df, _ = train_test_split(
        df,
        train_size=sample_size,
        stratify=df["income"],
        random_state=42,
    )

    X = sampled_df[selected_features].copy()
    encoder_map = {}
    for col in X.select_dtypes(include=["object", "string", "category"]).columns:
        enc = LabelEncoder()
        X[col] = enc.fit_transform(X[col].astype(str))
        encoder_map[col] = enc

    y = sampled_df["income"].astype(int).values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return (
        X_test,
        X_train,
        encoder_map,
        sample_size,
        selected_features,
        y_test,
        y_train,
    )


@app.cell
def _(selected_features):
    selected_features
    return


@app.cell(hide_code=True)
def _(
    X_test,
    X_train,
    encoder_map,
    mo,
    sample_size,
    selected_features,
    y_test,
):
    mo.md(f"""
    **Dataset ready**

    | | |
    |---|---|
    | Sampled rows used for modeling | `{sample_size:,}` |
    | Features selected | `{len(selected_features)}` |
    | Encoded columns | `{list(encoder_map)}` |
    | Training rows | `{X_train.shape[0]:,}` |
    | Test rows | `{X_test.shape[0]:,}` |
    | Positive class share (test) | `{y_test.mean():.1%}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Fit two models and compare probabilities

    Both models use the same selected features and the same train/test split.
    The useful comparison is not just the final score, but how the predicted
    probabilities and downstream plots change when you change the inputs.

    If TabICL feels slow during a live session, lower the sampled row count and
    run the comparison again. That faster change-and-observe loop is the main
    point of the notebook.
    """)
    return


@app.cell
def _(RandomForestClassifier, TabICLClassifier, X_test, X_train, mo, y_train):
    tabicl = TabICLClassifier()
    tabicl.fit(X_train, y_train)
    tabicl_proba = tabicl.predict_proba(X_test)

    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_proba = rf.predict_proba(X_test)

    mo.md(
        f"""
        Both models are fitted on `{X_train.shape[0]:,}` training rows.

        - `tabicl_proba[:, 1]` gives the estimated probability of income > 50K
          from TabICL
        - `rf_proba[:, 1]` gives the same probability from Random Forest
        """
    )
    return rf_proba, tabicl_proba


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Compare: ROC AUC

    ROC AUC summarises the ranking quality of predicted probabilities across
    all possible classification thresholds — it does not depend on a fixed
    cut-off like 0.5.

    - **1.0** → perfect ranking
    - **0.5** → random guessing

    This is a better metric than accuracy when classes are imbalanced, which
    is the case here: most people in the dataset earn ≤ 50K.
    """)
    return


@app.cell
def _(mo, plt, rf_proba, roc_auc_score, tabicl_proba, y_test):
    rf_auc = roc_auc_score(y_test, rf_proba[:, 1])
    tabicl_auc = roc_auc_score(y_test, tabicl_proba[:, 1])

    fig_auc, ax_auc = plt.subplots(figsize=(5.5, 3.5), constrained_layout=True)
    bars = ax_auc.bar(
        ["TabICL", "Random Forest"],
        [tabicl_auc, rf_auc],
        color=["#4C72B0", "#55A868"],
    )
    ax_auc.set_ylim(0.5, 1.0)
    ax_auc.set_ylabel("ROC AUC")
    ax_auc.set_title("Model comparison on the same dataset")
    for bar, value in zip(bars, [tabicl_auc, rf_auc]):
        ax_auc.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.01,
            f"{value:.3f}",
            ha="center",
        )

    mo.vstack(
        [
            mo.callout(
                mo.md(
                    f"**TabICL ROC AUC:** `{tabicl_auc:.3f}`\n\n"
                    f"**Random Forest ROC AUC:** `{rf_auc:.3f}`"
                ),
                kind="success",
            ),
            fig_auc,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Predicted probability distributions

    These histograms show how each model distributes its confidence across the
    test set. Comparing them makes it easier to see how the same data can lead
    to different probability behavior.

    Separate bars for each true label let you see whether each model assigns
    higher probabilities to the correct class.
    """)
    return


@app.cell
def _(np, plt, rf_proba, tabicl_proba, y_test):
    fig_hist, axes = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True, sharey=True)
    bins = np.linspace(0, 1, 30)
    plot_inputs = [
        ("TabICL", tabicl_proba, axes[0]),
        ("Random Forest", rf_proba, axes[1]),
    ]
    for title, proba, ax_hist in plot_inputs:
        for _label, _color, _name in [(0, "#4C72B0", "≤50K"), (1, "#DD8452", ">50K")]:
            ax_hist.hist(
                proba[y_test == _label, 1],
                bins=bins,
                alpha=0.65,
                color=_color,
                label=f"True label: {_name}",
            )
        ax_hist.set_xlabel("Predicted probability of income > 50K")
        ax_hist.set_ylabel("Count")
        ax_hist.set_title(title)
        ax_hist.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Error Analysis

    Adjust the probability threshold used to convert predictions into hard
    labels, then inspect which rows were misclassified. Lowering the threshold
    catches more high-income earners but increases false positives.

    This closes the loop from model outputs back to data — a key step in
    understanding where and why a model struggles.
    """)
    return


@app.cell
def _(mo):
    threshold_slider = mo.ui.slider(
        start=0.1,
        stop=0.9,
        step=0.05,
        value=0.5,
        label="Classification threshold",
        show_value=True,
    )
    model_source = mo.ui.radio(
        options=["TabICL", "Random Forest"],
        value="TabICL",
        label="Model to inspect",
    )
    model_view = mo.ui.radio(
        options=[
            "All errors",
            "False positives (predicted >50K, actually ≤50K)",
            "False negatives (predicted ≤50K, actually >50K)",
        ],
        value="All errors",
        label="Error type to inspect",
    )
    mo.vstack([model_source, threshold_slider, model_view])
    return model_source, model_view, threshold_slider


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    `mo.ui.radio(...)` chooses which model to inspect.
    `mo.ui.slider(...)` controls the probability threshold.
    `mo.ui.radio(...)` filters which error type appears in the table below.
    Both widgets feed the next cells reactively — no rerun needed.
    """)
    return


@app.cell
def _(
    X_test,
    mo,
    model_source,
    model_view,
    rf_proba,
    tabicl_proba,
    threshold_slider,
    y_test,
):
    threshold = threshold_slider.value
    active_proba = tabicl_proba if model_source.value == "TabICL" else rf_proba
    y_pred = (active_proba[:, 1] >= threshold).astype(int)

    results_df = X_test.copy()
    results_df["true_label"] = y_test
    results_df["predicted"] = y_pred
    results_df["proba_positive"] = active_proba[:, 1].round(3)
    results_df["correct"] = (results_df["true_label"] == results_df["predicted"]).astype(int)
    results_df["income_label"] = results_df["true_label"].map({0: "≤50K", 1: ">50K"})

    errors = results_df[results_df["correct"] == 0].copy()
    fp = errors[errors["predicted"] == 1]
    fn = errors[errors["predicted"] == 0]

    if "False positives" in model_view.value:
        display_errors = fp
    elif "False negatives" in model_view.value:
        display_errors = fn
    else:
        display_errors = errors

    n_correct = results_df["correct"].sum()
    n_total = len(results_df)
    mo.md(
        f"""
        **Model:** `{model_source.value}`

        **Threshold: `{threshold}`**

        | | Count |
        |---|---|
        | Correct predictions | `{n_correct:,}` / `{n_total:,}` (`{n_correct/n_total:.1%}`) |
        | All errors | `{len(errors):,}` |
        | False positives | `{len(fp):,}` |
        | False negatives | `{len(fn):,}` |
        """
    )
    return (display_errors,)


@app.cell
def _(display_errors, mo, preview_rows):
    display_cols = [
        col
        for col in [
            "age",
            "education-num",
            "hours-per-week",
            "capital-gain",
            "proba_positive",
            "income_label",
            "predicted",
        ]
        if col in display_errors.columns
    ]
    error_table = mo.ui.table(
        display_errors[display_cols].head(preview_rows.value),
        label="Select misclassified rows to inspect",
    )
    error_table
    return


if __name__ == "__main__":
    app.run()
