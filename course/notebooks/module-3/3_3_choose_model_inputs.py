# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==6.0.0",
#     "marimo==0.23.16",
#     "pandas==2.3.3",
#     "pyarrow==24.0.0",
#     "scikit-learn==1.8.0",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Choose model inputs

    This notebook includes the data tools from sections 3.1 and 3.2. It adds controls for the features and rows used for modeling.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    return LabelEncoder, mo, pd, train_test_split


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
    ## Inspect and edit data
    """)
    return


@app.cell
def _(df):
    df[:1000]
    return


@app.cell
def _(df, mo):
    data_editor = mo.ui.data_editor(data=df.head(20))
    data_editor
    return (data_editor,)


@app.cell
def _(data_editor):
    edited_df = data_editor.value
    edited_df
    return


@app.cell
def _(df, mo):
    table = mo.ui.table(data=df.head(100), selection="multi")
    table
    return (table,)


@app.cell
def _(table):
    selected_rows = table.value
    selected_rows
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Explore data visually
    """)
    return


@app.cell
def _(df, mo):
    data_explorer = mo.ui.data_explorer(df)
    data_explorer
    return


@app.cell
def _(df, mo):
    dataframe = mo.ui.dataframe(df)
    dataframe
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Select features
    """)
    return


@app.cell
def _(feature_options, mo):
    selected_features_ui = mo.ui.multiselect(
        options=feature_options,
        value=feature_options,
        label="Features to include in the model",
    )
    selected_features_ui
    return (selected_features_ui,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose a sample size
    """)
    return


@app.cell
def _(mo):
    sample_size_ui = mo.ui.slider(
        start=500,
        stop=3000,
        step=500,
        value=1000,
        label="Rows to sample for modeling",
        show_value=True,
    )
    sample_size_ui
    return (sample_size_ui,)


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
    for column in X.select_dtypes(include=["object", "category"]).columns:
        encoder = LabelEncoder()
        X[column] = encoder.fit_transform(X[column].astype(str))
        encoder_map[column] = encoder

    y = sampled_df["income"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    return X_test, X_train, encoder_map, sample_size, selected_features, y_test, y_train


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
    | Sampled rows | `{sample_size:,}` |
    | Selected features | `{len(selected_features)}` |
    | Encoded columns | `{list(encoder_map)}` |
    | Training rows | `{X_train.shape[0]:,}` |
    | Test rows | `{X_test.shape[0]:,}` |
    | Test rows above $50K | `{y_test.mean():.1%}` |
    """)
    return


if __name__ == "__main__":
    app.run()
