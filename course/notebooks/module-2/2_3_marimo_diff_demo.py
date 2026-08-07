import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Small code change, small diff

    marimo notebooks are plain Python files — no JSON, no embedded outputs.
    `git diff` shows only the lines you actually changed.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Try it in this embed:** change `power = 3` to `power = 4` and run the cell. The plot updates immediately.

    To inspect the source change with Git, open a copy of this notebook locally inside a Git project. Open marimo's **Terminal** tab from the developer panel, change and save the value, then run:

    ```bash
    git diff -- your_notebook.py
    ```

    Replace `your_notebook.py` with the notebook's filename. The diff shows the changed Python line and does not include the regenerated plot. The course embed has no Git history, so run this part in a locally tracked notebook.
    """)
    return


@app.cell
def _():
    power = 3
    return (power,)


@app.cell
def _(np, plt, power):
    rng = np.random.default_rng(7)
    x = np.linspace(-3, 3, 800)
    curve = x**power
    noisy_curve = curve + rng.normal(scale=0.8, size=x.size)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=140)
    ax.scatter(x, noisy_curve, s=8, alpha=0.35, label="simulated observations")
    ax.plot(x, curve, color="black", linewidth=2.5, label=f"x^{power}")
    ax.axhline(0, color="0.85", linewidth=1)
    ax.axvline(0, color="0.85", linewidth=1)
    ax.set_title(f"Model curve: y = x^{power}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    fig
    return


if __name__ == "__main__":
    app.run()
