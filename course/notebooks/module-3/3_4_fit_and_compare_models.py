# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.23.16",
#     "matplotlib==3.10.7",
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
    # Fit and compare models

    Choose the model inputs. Then train TabICL and Random Forest on the same rows and compare their results.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.datasets import fetch_openml
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
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
    ## Choose the inputs

    Start with 1,000 rows and all features. You can change either control after the first model comparison.
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
    return X_test, X_train, selected_features, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Train TabICL and Random Forest

    Let's train both models with the same training and test rows. Each model returns a probability that income is above $50K.
    """)
    return


@app.cell
def _(RandomForestClassifier, TabICLClassifier, X_test, X_train, mo, y_train):
    tabicl = TabICLClassifier()
    tabicl.fit(X_train, y_train)
    tabicl_proba = tabicl.predict_proba(X_test)

    random_forest = RandomForestClassifier(n_estimators=200, random_state=42)
    random_forest.fit(X_train, y_train)
    rf_proba = random_forest.predict_proba(X_test)

    mo.md(f"Both models were trained on `{X_train.shape[0]:,}` rows.")
    return rf_proba, tabicl_proba


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compare ROC AUC

    Let's compare the models with ROC AUC. A score of `1.0` is perfect. A score of `0.5` is no better than random ranking.
    """)
    return


@app.cell
def _(mo, plt, rf_proba, roc_auc_score, tabicl_proba, y_test):
    tabicl_auc = roc_auc_score(y_test, tabicl_proba[:, 1])
    rf_auc = roc_auc_score(y_test, rf_proba[:, 1])

    fig_auc, ax_auc = plt.subplots(figsize=(5.5, 3.5), constrained_layout=True)
    bars = ax_auc.bar(
        ["TabICL", "Random Forest"],
        [tabicl_auc, rf_auc],
        color=["#4C72B0", "#55A868"],
    )
    ax_auc.set_ylim(0.5, 1.0)
    ax_auc.set_ylabel("ROC AUC")
    ax_auc.set_title("Model comparison")
    for bar, value in zip(bars, [tabicl_auc, rf_auc]):
        ax_auc.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.01,
            f"{value:.3f}",
            ha="center",
        )

    mo.vstack(
        [
            mo.md(
                f"**TabICL:** `{tabicl_auc:.3f}`  \n"
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

    Compare how the models distribute their predicted probabilities across the two true income groups.
    """)
    return


@app.cell
def _(np, plt, rf_proba, tabicl_proba, y_test):
    fig_hist, axes = plt.subplots(
        1,
        2,
        figsize=(11, 3.8),
        constrained_layout=True,
        sharey=True,
    )
    bins = np.linspace(0, 1, 30)
    for title, probabilities, axis in [
        ("TabICL", tabicl_proba, axes[0]),
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
