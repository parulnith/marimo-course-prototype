# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai", "pandas"]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import json
    import marimo as mo
    import pandas as pd
    from openai import OpenAI


@app.function
def get_client(base_url="http://localhost:11434/v1/"):
    return OpenAI(base_url=base_url, api_key="ollama")


@app.function
def compare_two_models(client, texts, model_a, model_b):
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


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Reuse classifier functions

    `get_client()` and `compare_two_models()` are marked with `@app.function` so another
    Python file or marimo notebook can import them.
    """)
    return


@app.cell
def _(get_client):
    get_client()
    return


if __name__ == "__main__":
    app.run()
