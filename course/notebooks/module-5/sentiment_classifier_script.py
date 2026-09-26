# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "marimo",
#   "pandas",
#   "requests",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import argparse
    import marimo as mo
    import sys

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
{"label": "positive", "reason": "one sentence"}.
The label must be exactly positive, negative, or neutral. Do not use any other label."""


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Run the sentiment classifier as a script

    This version receives the model names and output filename from the command
    line. It classifies the reviews and saves the results to a CSV file without
    opening the notebook interface.
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
                response = requests.post(
                    "http://localhost:11434/v1/chat/completions",
                    headers={"Authorization": "Bearer ollama"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": text},
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                answer = json.loads(
                    response.json()["choices"][0]["message"]["content"] or "{}"
                )
                label = str(answer.get("label", "error")).strip().lower()
                rows.append(
                    {
                        "text": text,
                        "model": model,
                        "label": label
                        if label in {"positive", "negative", "neutral"}
                        else "error",
                        "reason": answer.get("reason", ""),
                    }
                )
            except Exception as exc:
                rows.append(
                    {
                        "text": text,
                        "model": model,
                        "label": "error",
                        "reason": str(exc),
                    }
                )
    return pd.DataFrame(rows)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The script accepts three options:

    - `--model-a` chooses the first model.
    - `--model-b` chooses the second model.
    - `--output` names the CSV file.
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
        run_as_script(sys.argv[sys.argv.index("--") + 1 :])
    else:
        app.run()
