# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.3",
#     "mcp==1.27.1",
#     "pandas==2.3.3",
#     "scikit-learn==1.8.0",
# ]
# ///

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/parulnith/marimo-course-prototype/blob/main/course/notebooks/module-2/2_2_sandboxed_environment.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # The "It Works on My Machine" Problem
    """)
    return


@app.cell
def _():
    import marimo as mo
    import sys
    import sklearn

    return mo, sklearn, sys


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Example 1: scikit-learn 1.8 feature change
    """)
    return


@app.cell
def _(sklearn, sys):
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    print(f"python executable: {sys.executable}")
    print(f"python version: {sys.version.split()[0]}")
    print(f"sklearn version: {sklearn.__version__}")

    X, y = make_classification(n_samples=300, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    base_model = LogisticRegression(max_iter=1000)
    model = CalibratedClassifierCV(base_model, method="temperature", cv=3)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    print("temperature calibration is available in this environment")
    print(f"accuracy: {accuracy:.3f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Example 2: pandas API change
    """)
    return


@app.cell
def _():
    from io import StringIO
    import pandas as pd

    print(f"pandas version: {pd.__version__}")

    csv_data = """feature_a feature_b label
    1 10 0
    2 20 1
    3 30 0
    """
    df = pd.read_csv(StringIO(csv_data), delim_whitespace=True)
    print(df)
    return


if __name__ == "__main__":
    app.run()
