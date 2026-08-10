# pyright: reportMissingImports=false

import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np

    return np, plt


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
