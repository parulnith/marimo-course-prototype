# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.1",
#     "pandas",
#     "scikit-learn",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Module 3 starter: connect data, controls, and a model

    This notebook uses a small classification dataset included with
    scikit-learn. Change the controls and watch the model summary and error
    table update.

    You can also add cells while you work through the lesson. Try the
    dataframe editor and data explorer when the lesson introduces them.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from sklearn.datasets import load_breast_cancer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split

    return (
        RandomForestClassifier,
        load_breast_cancer,
        mo,
        pd,
        roc_auc_score,
        train_test_split,
    )


@app.cell
def _(load_breast_cancer):
    dataset = load_breast_cancer(as_frame=True)
    df = dataset.frame.copy()
    df["diagnosis"] = df["target"].map({0: "malignant", 1: "benign"})
    feature_options = list(dataset.feature_names)
    return df, feature_options


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Inspect the data

    Use the table below to sort and filter the rows. Add a new cell and enter
    `mo.ui.data_editor(df.head(20))` when you reach the data editor activity.
    """)
    return


@app.cell
def _(df, mo):
    data_view = mo.ui.dataframe(df)
    data_view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Add another cell containing `mo.ui.data_explorer(df)` during the visual
    exploration activity. Use `diagnosis` to compare the two classes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Control the model

    The feature selector and sample size are inputs to the model cell. The
    threshold becomes an input to the error analysis.
    """)
    return


@app.cell
def _(feature_options, mo):
    feature_selector = mo.ui.multiselect(
        options=feature_options,
        value=feature_options[:6],
        label="Features to include",
    )
    sample_size = mo.ui.slider(
        start=200,
        stop=500,
        step=100,
        value=300,
        label="Rows to use",
        show_value=True,
    )
    threshold = mo.ui.slider(
        start=0.1,
        stop=0.9,
        step=0.05,
        value=0.5,
        label="Classification threshold",
        show_value=True,
    )
    mo.vstack([feature_selector, sample_size, threshold])
    return feature_selector, sample_size, threshold


@app.cell
def _(
    RandomForestClassifier,
    df,
    feature_selector,
    roc_auc_score,
    sample_size,
    train_test_split,
):
    selected_features = feature_selector.value
    sampled_df, _ = train_test_split(
        df,
        train_size=sample_size.value,
        stratify=df["target"],
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        sampled_df[selected_features],
        sampled_df["target"],
        test_size=0.25,
        stratify=sampled_df["target"],
        random_state=42,
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    probability = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probability)
    return X_test, auc, probability, selected_features, y_test


@app.cell(hide_code=True)
def _(X_test, auc, mo, sample_size, selected_features):
    mo.md(f"""
    **Model summary**

    | | |
    |---|---|
    | Rows sampled | `{sample_size.value}` |
    | Features selected | `{len(selected_features)}` |
    | Test rows | `{len(X_test)}` |
    | ROC AUC | `{auc:.3f}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inspect errors

    Move the threshold and compare the error counts. The model probabilities
    stay the same, while the predicted classes and error table update.
    """)
    return


@app.cell
def _(X_test, mo, pd, probability, threshold, y_test):
    prediction = (probability >= threshold.value).astype(int)
    results = X_test.copy()
    results["true_label"] = y_test.map({0: "malignant", 1: "benign"})
    results["predicted_label"] = pd.Series(
        prediction, index=X_test.index
    ).map({0: "malignant", 1: "benign"})
    results["probability_benign"] = probability.round(3)
    results["error_type"] = "correct"
    results.loc[
        (y_test == 0) & (prediction == 1), "error_type"
    ] = "false positive"
    results.loc[
        (y_test == 1) & (prediction == 0), "error_type"
    ] = "false negative"
    errors = results[results["error_type"] != "correct"]
    false_positives = (results["error_type"] == "false positive").sum()
    false_negatives = (results["error_type"] == "false negative").sum()
    mo.vstack(
        [
            mo.md(
                f"""
                **Threshold:** `{threshold.value}`

                | Error type | Count |
                |---|---:|
                | False positives | `{false_positives}` |
                | False negatives | `{false_negatives}` |
                """
            ),
            mo.ui.table(errors.head(20), label="Misclassified rows"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Continue the exercise

    Add a cell below and try one of these changes:

    - Display `feature_selector.value`.
    - Replace Random Forest with another scikit-learn classifier.
    - Create a chart from the error table.
    """)
    return


if __name__ == "__main__":
    app.run()
