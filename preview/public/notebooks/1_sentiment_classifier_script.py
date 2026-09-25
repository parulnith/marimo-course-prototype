# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas"]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import argparse
    import json
    import marimo as mo
    import pandas as pd
    from openai import OpenAI

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


@app.function
def compare_two_models(texts, model_a, model_b):
    client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")
    rows = []
    for text in texts:
        for model in (model_a, model_b):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": "Return only JSON with label, confidence, and reason. The label must be exactly positive, negative, or neutral."}, {"role": "user", "content": text}],
                    response_format={"type": "json_object"},
                    temperature=0,
                )
                answer = json.loads(response.choices[0].message.content or "{}")
                label = str(answer.get("label", "error")).strip().lower()
                rows.append({"text": text, "model": model, "label": label if label in {"positive", "negative", "neutral"} else "error", "confidence": answer.get("confidence", 0), "reason": answer.get("reason", "")})
            except Exception as exc:
                rows.append({"text": text, "model": model, "label": "error", "confidence": 0, "reason": str(exc)})
    return pd.DataFrame(rows)


@app.function
def run_headless(argv):
    parser = argparse.ArgumentParser(description="Compare two models on product reviews.")
    parser.add_argument("--model-a", default="gemma3:1b")
    parser.add_argument("--model-b", default="qwen3:1.7b")
    parser.add_argument("--output", default="results.csv")
    args = parser.parse_args(argv)
    results = compare_two_models(REVIEWS, args.model_a, args.model_b)
    results.to_csv(args.output, index=False)
    print(f"Wrote {len(results)} rows to {args.output}")


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Run the classifier as a script

    This file accepts model names and an output path from the command line.
    Run `uv run python 1_sentiment_classifier_script.py -- --output results.csv`.
    """)
    return


@app.cell
def _():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--model-a", default="gemma3:1b")
    parser.add_argument("--model-b", default="qwen3:1.7b")
    args, _ = parser.parse_known_args()
    return (args,)


@app.cell
def _(args, compare_two_models):
    compare_two_models(REVIEWS, args.model_a, args.model_b)
    return


if __name__ == "__main__":
    import sys

    if "--" in sys.argv:
        run_headless(sys.argv[sys.argv.index("--") + 1 :])
    else:
        app.run()
