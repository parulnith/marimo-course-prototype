# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.23.16",
#     "numpy",
#     "pandas==2.3.3",
#     "scikit-learn==1.8.0",
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
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    return (
        DecisionTreeClassifier,
        LabelEncoder,
        RandomForestClassifier,
        mo,
        pd,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(pd):
    adult_csv_url = "https://www.openml.org/data/get_csv/1595261/phpMawTba"
    df = pd.read_csv(adult_csv_url, na_values="?", skipinitialspace=True)
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    return (df,)


@app.cell(hide_code=True)
def _(
    LabelEncoder,
    df,
    train_test_split,
):
    selected_features = [column for column in df.columns if column != "income"]
    sampled_df, _ = train_test_split(
        df,
        train_size=1000,
        stratify=df["income"],
        random_state=42,
    )

    X = sampled_df[selected_features].copy()
    for column in X.select_dtypes(include=["object", "string", "category"]).columns:
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
def _(DecisionTreeClassifier, RandomForestClassifier, X_test, X_train, y_train):
    decision_tree = DecisionTreeClassifier(max_depth=5, random_state=42)
    decision_tree.fit(X_train, y_train)
    tree_proba = decision_tree.predict_proba(X_test)

    random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
    random_forest.fit(X_train, y_train)
    rf_proba = random_forest.predict_proba(X_test)
    return rf_proba, tree_proba


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose a model and threshold

    The threshold converts a probability into a class prediction. A row is predicted to have income above $50K when its probability is at or above the threshold. Change the threshold and inspect the updated error counts.

    A false positive is a person predicted to earn above $50K whose true label is at or below $50K. A false negative is a person predicted to earn at or below $50K whose true label is above $50K.

    Raising the threshold usually reduces false positives and increases false negatives. The best threshold depends on which error has a larger cost for the problem you are solving.
    """)
    return


@app.cell
def _(mo):
    model_source = mo.ui.radio(
        options=["Decision Tree", "Random Forest"],
        value="Decision Tree",
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
    test_rows,
    threshold_slider,
    tree_proba,
    y_test,
):
    probabilities = tree_proba if model_source.value == "Decision Tree" else rf_proba
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

    Select a few rows and compare their features. This takes you from an overall score back to the data behind the score.
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
    Use the selected errors to choose the next experiment. You can adjust the threshold here or return to the model comparison and change the features.
    """)
    return


if __name__ == "__main__":
    app.run()
