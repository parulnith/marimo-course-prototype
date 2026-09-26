# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "marimo",
#   "pandas",
#   "requests",
#   "pyodide-http; sys_platform == 'emscripten'",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import argparse
    import marimo as mo
    import sys

    if sys.platform == "emscripten":
        import pyodide_http

        pyodide_http.patch_all()

    REVIEWS = [
        "Oh wonderful, another charger that lasts a whole three weeks. Just what I needed.",
        "The product itself is fantastic, but the courier left it in the rain.",
        "Not bad. Not great. I keep using it, which probably says something.",
        "I wanted to hate this but I can't. Annoyingly good.",
        "Five stars for the packaging. The thing inside? Different story.",
        "Does exactly what the listing says. That is neither a compliment nor a complaint.",
        "Returned it. Then bought it again. Make of that what you will.",
        "If you enjoy reading 40-page manuals to brew coffee, this is the product for you.",
        "Customer service was great. Shame I had to call them four times.",
        "Honestly underwhelming for the price, but I can see why some people love it.",
        "Build quality is solid, instructions are terrible.",
        "It works. My cat is unimpressed. I am cautiously optimistic.",
    ]
    SYSTEM_PROMPT = """Classify the product review. Return only JSON in this exact form:
{"label": "positive", "confidence": 0.0, "reason": "one sentence"}.
The label must be exactly positive, negative, or neutral. Do not use any other label."""


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Product review sentiment classifier

    Classify the same twelve product reviews with two local models and compare their results.
    """)
    return


@app.function(hide_code=True)
def compare_reviews(texts, model_a, model_b):
    import json

    import pandas as pd
    import requests

    rows = []
    for model in (model_a, model_b):
        for text in texts:
            try:
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ]
                response = requests.post(
                    "http://localhost:11434/v1/chat/completions",
                    headers={"Authorization": "Bearer ollama"},
                    json={
                        "model": model,
                        "messages": messages,
                        "response_format": {"type": "json_object"},
                        "temperature": 0,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                answer = json.loads(content or "{}")
                label = str(answer.get("label", "error")).strip().lower()
                rows.append({
                    "text": text,
                    "model": model,
                    "label": label if label in {"positive", "negative", "neutral"} else "error",
                    "confidence": round(float(answer.get("confidence", 0)), 3),
                    "reason": answer.get("reason", ""),
                })
            except Exception as exc:
                rows.append({"text": text, "model": model, "label": "error", "confidence": 0, "reason": str(exc)})
    return pd.DataFrame(rows)


@app.cell
def _(mo):
    model_a = mo.ui.text(value="gemma3:1b", label="Model A")
    model_b = mo.ui.text(value="qwen3:1.7b", label="Model B")
    reviews = mo.ui.text_area(value="\n".join(REVIEWS), label="Reviews, one per line", rows=10, full_width=True)
    run = mo.ui.run_button(label="Classify with both models", kind="success")
    return model_a, model_b, reviews, run


@app.cell
def _(mo, model_a, model_b, reviews, run):
    mo.vstack([
        mo.hstack([model_a, model_b]),
        reviews,
        run,
    ])
    return


@app.cell
def _(compare_reviews, model_a, model_b, mo, reviews, run):
    mo.stop(not run.value, mo.md("Select **Classify with both models** to begin."))
    texts = [text.strip() for text in reviews.value.splitlines() if text.strip()]
    results = compare_reviews(texts, model_a.value, model_b.value)
    results
    return (results,)


@app.cell
def _(mo, results):
    comparison = results.pivot(
        index="text",
        columns="model",
        values=["label", "confidence", "reason"],
    )
    comparison.columns = [f"{model}: {field}" for field, model in comparison.columns]
    comparison = comparison.reset_index()
    mo.vstack([
        mo.md("## Compare each review side by side"),
        comparison,
    ])
    return (comparison,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Run the notebook as a script

    The notebook controls are useful when a person runs the classifier. The
    function below provides another way to start the same work from the command
    line. It reads the model names and output filename, calls
    `compare_reviews()`, and saves the results as a CSV file.

    The final block in the notebook checks for `--`. If it finds `--`, it calls
    `run_as_script()`. Otherwise, marimo opens the notebook in the editor.

    ```python
    if __name__ == "__main__":
        if "--" in sys.argv:
            run_as_script(sys.argv[sys.argv.index("--") + 1:])
        else:
            app.run()
    ```
    """)
    return


@app.function
def run_as_script(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-a", default="gemma3:1b")
    parser.add_argument("--model-b", default="qwen3:1.7b")
    parser.add_argument("--output", default="results.csv")
    args = parser.parse_args(argv)

    results = compare_reviews(REVIEWS, args.model_a, args.model_b)
    results.to_csv(args.output, index=False)
    print(f"Wrote {len(results)} rows to {args.output}")


if __name__ == "__main__":
    if "--" in sys.argv:
        run_as_script(sys.argv[sys.argv.index("--") + 1:])
    else:
        app.run()
