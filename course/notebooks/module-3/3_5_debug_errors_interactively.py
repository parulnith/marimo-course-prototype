# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.23.16",
#     "numpy",
#     "pandas==2.3.3",
#     "scikit-learn==1.8.0",
#     "tabicl",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Debug errors interactively

    Choose the model and classification threshold. Then inspect the rows that the model classified incorrectly.
    """)
    return


@app.cell
def _():
    import marimo as mo
    from sklearn.datasets import fetch_openml
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from tabicl import TabICLClassifier

    return (
        LabelEncoder,
        RandomForestClassifier,
        TabICLClassifier,
        fetch_openml,
        mo,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(fetch_openml):
    data = fetch_openml("adult", version=2, as_frame=True)
    df = data.frame.copy()
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    feature_options = [column for column in df.columns if column != "income"]
    return df, feature_options


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model inputs

    These controls feed the model training cells. Change them after inspecting the first set of errors.
    """)
    return


@app.cell
def _(feature_options, mo):
    selected_features_ui = mo.ui.multiselect(
        options=feature_options,
        value=feature_options,
        label="Features to include",
    )
    sample_size_ui = mo.ui.slider(
        start=500,
        stop=3000,
        step=500,
        value=1000,
        label="Rows to sample",
        show_value=True,
    )
    mo.vstack([selected_features_ui, sample_size_ui])
    return sample_size_ui, selected_features_ui


@app.cell(hide_code=True)
def _(
    LabelEncoder,
    df,
    sample_size_ui,
    selected_features_ui,
    train_test_split,
):
    selected_features = selected_features_ui.value
    sampled_df, _ = train_test_split(
        df,
        train_size=sample_size_ui.value,
        stratify=df["income"],
        random_state=42,
    )

    X = sampled_df[selected_features].copy()
    for column in X.select_dtypes(include=["object", "category"]).columns:
        encoder = LabelEncoder()
        X[column] = encoder.fit_transform(X[column].astype(str))

    y = sampled_df["income"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    test_rows = sampled_df.loc[X_test.index, selected_features].copy()
    return X_test, X_train, test_rows, y_test, y_train


@app.cell(hide_code=True)
def _(RandomForestClassifier, TabICLClassifier, X_test, X_train, y_train):
    tabicl = TabICLClassifier()
    tabicl.fit(X_train, y_train)
    tabicl_proba = tabicl.predict_proba(X_test)

    random_forest = RandomForestClassifier(n_estimators=200, random_state=42)
    random_forest.fit(X_train, y_train)
    rf_proba = random_forest.predict_proba(X_test)
    return rf_proba, tabicl_proba


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose a model and threshold

    The threshold converts a probability into a class prediction. Change it and inspect the updated error counts.
    """)
    return


@app.cell
def _(mo):
    model_source = mo.ui.radio(
        options=["TabICL", "Random Forest"],
        value="TabICL",
        label="Model to inspect",
    )
    threshold_slider = mo.ui.slider(
        start=0.1,
        stop=0.9,
        step=0.05,
        value=0.5,
        label="Classification threshold",
        show_value=True,
    )
    error_type = mo.ui.radio(
        options=["All errors", "False positives", "False negatives"],
        value="All errors",
        label="Error type",
    )
    mo.vstack([model_source, threshold_slider, error_type])
    return error_type, model_source, threshold_slider


@app.cell
def _(
    error_type,
    model_source,
    rf_proba,
    tabicl_proba,
    test_rows,
    threshold_slider,
    y_test,
):
    probabilities = tabicl_proba if model_source.value == "TabICL" else rf_proba
    predictions = (probabilities[:, 1] >= threshold_slider.value).astype(int)

    results = test_rows.copy()
    results["true_label"] = y_test.to_numpy()
    results["predicted"] = predictions
    results["probability_above_50k"] = probabilities[:, 1].round(3)

    false_positives = results[
        (results["true_label"] == 0) & (results["predicted"] == 1)
    ]
    false_negatives = results[
        (results["true_label"] == 1) & (results["predicted"] == 0)
    ]
    errors = results[results["true_label"] != results["predicted"]]

    if error_type.value == "False positives":
        displayed_errors = false_positives
    elif error_type.value == "False negatives":
        displayed_errors = false_negatives
    else:
        displayed_errors = errors

    error_counts = {
        "all": len(errors),
        "false_positives": len(false_positives),
        "false_negatives": len(false_negatives),
    }
    return displayed_errors, error_counts


@app.cell
def _(error_counts, mo, model_source, threshold_slider):
    mo.md(f"""
    **Model:** `{model_source.value}`

    **Threshold:** `{threshold_slider.value}`

    | Error type | Count |
    |---|---:|
    | All errors | `{error_counts['all']}` |
    | False positives | `{error_counts['false_positives']}` |
    | False negatives | `{error_counts['false_negatives']}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect the errors

    Select a few rows and compare their features.
    """)
    return


@app.cell
def _(displayed_errors, mo):
    display_columns = [
        column
        for column in [
            "age",
            "education",
            "occupation",
            "hours-per-week",
            "capital-gain",
            "probability_above_50k",
            "true_label",
            "predicted",
        ]
        if column in displayed_errors.columns
    ]
    error_table = mo.ui.table(
        data=displayed_errors[display_columns].head(20),
        selection="multi",
        label="Select errors to inspect",
    )
    error_table
    return (error_table,)


@app.cell
def _(error_table):
    selected_errors = error_table.value
    selected_errors
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use the selected errors to choose the next experiment. You could change a feature, use more rows, or adjust the threshold.
    """)
    return


if __name__ == "__main__":
    app.run()
