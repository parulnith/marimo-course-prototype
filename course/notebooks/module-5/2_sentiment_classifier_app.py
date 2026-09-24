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
def classify_reviews(texts, model_a, model_b):
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


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Publish the classifier as an app

    Run `marimo run 2_sentiment_classifier_app.py` to give someone this interface without code cells.
    """)
    return


@app.cell
def _(mo):
    model_a = mo.ui.text(value="gemma3:1b", label="Model A")
    model_b = mo.ui.text(value="qwen2.5:0.5b", label="Model B")
    reviews = mo.ui.text_area(value="\n".join(REVIEWS), label="Reviews, one per line", rows=10, full_width=True)
    run = mo.ui.run_button(label="Classify", kind="success")
    mo.vstack([mo.hstack([model_a, model_b]), reviews, run])
    return model_a, model_b, reviews, run


@app.cell
def _(classify_reviews, model_a, model_b, mo, reviews, run):
    mo.stop(not run.value, mo.md("Enter reviews and select **Classify**."))
    texts = [text.strip() for text in reviews.value.splitlines() if text.strip()]
    classify_reviews(texts, model_a.value, model_b.value)
    return


if __name__ == "__main__":
    app.run()
