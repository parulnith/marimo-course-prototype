import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    a = 1
    return (a,)


@app.cell
def _():
    b = 2
    return (b,)


@app.cell
def _(a, b):
    a + b
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
