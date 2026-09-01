# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.23.16",
#     "matplotlib==3.10.7",
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
    # Train and evaluate models

    Let's use marimo controls to choose the model inputs, then train and evaluate a Decision Tree and Random Forest. Change a control and watch the model results update.

    ## Import the libraries

    First, let's import marimo, the data libraries, and the scikit-learn tools needed to prepare the data, train both models, and calculate their scores.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    return (
        DecisionTreeClassifier,
        LabelEncoder,
        RandomForestClassifier,
        mo,
        np,
        pd,
        plt,
        roc_auc_score,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the data

    Let's load the Adult Income dataset into `df`. We will convert the income label to `0` for income at or below $50K and `1` for income above $50K. We will also create a list of the columns that can be used as model features.
    """)
    return


@app.cell
def _(pd):
    adult_csv_url = "https://www.openml.org/data/get_csv/1595261/phpMawTba"
    df = pd.read_csv(adult_csv_url, na_values="?", skipinitialspace=True)
    df["income"] = (df["class"].str.strip() == ">50K").astype(int)
    df = df.drop(columns=["class"]).dropna()
    feature_options = [column for column in df.columns if column != "income"]
    return df, feature_options


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose the model inputs

    Different feature combinations may produce different model results. The sample size can also affect the scores and training time. The controls below let you test both choices without editing the model code.

    `mo.ui.multiselect()` creates marimo's multiselect control. It lets you choose several features from one list. Its `options` contain every available feature, and its `value` sets the initial selection.

    We can use `mo.ui.slider()` again, this time to control the sample size. The `start`, `stop`, and `step` arguments define the available values. `show_value=True` displays the current value beside the slider.

    `mo.vstack()` places both controls in one vertical layout. Both controls are connected to the data preparation and model results below.
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
def _(mo):
    mo.md(r"""
    ## Prepare the training and test data

    The next cell reads the current feature selection and sample size through each control's `.value`. It samples the requested number of rows, converts text categories into numbers, and creates one training and test split.

    Both models will use the same split. When you change either control, marimo runs this cell again before retraining the models.
    """)
    return


@app.cell
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
    return X_test, X_train, selected_features, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Train a Decision Tree and Random Forest

    A Decision Tree learns one set of rules from the training data. Random Forest combines predictions from many decision trees. Let's fit both models with the same training and test rows. Each model returns a probability that income is above $50K.
    """)
    return


@app.cell
def _(DecisionTreeClassifier, RandomForestClassifier, X_test, X_train, mo, y_train):
    decision_tree = DecisionTreeClassifier(max_depth=5, random_state=42)
    decision_tree.fit(X_train, y_train)
    tree_proba = decision_tree.predict_proba(X_test)

    random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
    random_forest.fit(X_train, y_train)
    rf_proba = random_forest.predict_proba(X_test)

    mo.md(f"Both models were fitted on `{X_train.shape[0]:,}` rows.")
    return rf_proba, tree_proba


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare ROC AUC

    Let's compare how well the models rank the two income groups. ROC AUC measures this ranking across all possible classification thresholds. A score of `1.0` is perfect. A score of `0.5` is no better than random ranking.
    """)
    return


@app.cell
def _(mo, plt, rf_proba, roc_auc_score, tree_proba, y_test):
    tree_auc = roc_auc_score(y_test, tree_proba[:, 1])
    rf_auc = roc_auc_score(y_test, rf_proba[:, 1])

    fig_auc, ax_auc = plt.subplots(figsize=(5.5, 3.5), constrained_layout=True)
    bars = ax_auc.bar(
        ["Decision Tree", "Random Forest"],
        [tree_auc, rf_auc],
        color=["#4C72B0", "#55A868"],
    )
    ax_auc.set_ylim(0.5, 1.0)
    ax_auc.set_ylabel("ROC AUC")
    ax_auc.set_title("Model comparison")
    for bar, value in zip(bars, [tree_auc, rf_auc]):
        ax_auc.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.01,
            f"{value:.3f}",
            ha="center",
        )

    mo.vstack(
        [
            mo.md(
                f"**Decision Tree:** `{tree_auc:.3f}`  \n"
                f"**Random Forest:** `{rf_auc:.3f}`"
            ),
            fig_auc,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspect predicted probabilities

    The probability plots show how each model distributes its predictions across the two true income groups. Two models can have similar ROC AUC scores and still assign different probabilities to the same test rows.
    """)
    return


@app.cell
def _(np, plt, rf_proba, tree_proba, y_test):
    fig_hist, axes = plt.subplots(
        1,
        2,
        figsize=(11, 3.8),
        constrained_layout=True,
        sharey=True,
    )
    bins = np.linspace(0, 1, 30)
    for title, probabilities, axis in [
        ("Decision Tree", tree_proba, axes[0]),
        ("Random Forest", rf_proba, axes[1]),
    ]:
        for label, color, name in [
            (0, "#4C72B0", "At or below $50K"),
            (1, "#DD8452", "Above $50K"),
        ]:
            axis.hist(
                probabilities[y_test.to_numpy() == label, 1],
                bins=bins,
                alpha=0.65,
                color=color,
                label=name,
            )
        axis.set_xlabel("Probability of income above $50K")
        axis.set_ylabel("Count")
        axis.set_title(title)
        axis.legend()
    fig_hist
    return


if __name__ == "__main__":
    app.run()
