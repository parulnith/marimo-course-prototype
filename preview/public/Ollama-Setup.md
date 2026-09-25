# Ollama Setup Handout

**Module 4**

Use this handout to set up Ollama locally and run a small model from the command line.

---

## What You Need

- Basic command-line comfort (`bash`, `zsh`, or similar)
- A laptop with enough free disk space for local models
- A recent Python environment only if you want to run the optional Python API check

---

## Setup Checklist

### 1. Install Ollama locally

Download Ollama here:  
[https://ollama.com/download](https://ollama.com/download)

Then confirm the install:

```bash
ollama --version
```

### 2. Start Ollama

If needed, start the local server:

```bash
ollama serve
```

No sign-in or API key is required for local models served at `http://localhost:11434`.

### 3. Download the example models

```bash
ollama pull gemma3:1b
ollama pull qwen3:1.7b
```

### 4. Run a quick test

```bash
ollama run gemma3:1b
```

Type `/bye` to exit the interactive model session.

### 5. Connect Ollama to marimo

In marimo, open notebook settings, go to the **AI** tab, and choose Ollama as an AI provider. For local Ollama, use the OpenAI-compatible endpoint:

```text
http://127.0.0.1:11434/v1
```

If editing `marimo.toml` directly, use:

```toml
[ai.models]
chat_model = "ollama/gemma3:1b"
edit_model = "ollama/gemma3:1b"
autocomplete_model = "ollama/gemma3:1b"

[ai.ollama]
base_url = "http://127.0.0.1:11434/v1"
```

The `/v1` suffix matters for marimo because marimo talks to Ollama through Ollama's OpenAI-compatible API.

---

## Commands At A Glance

```bash
ollama --version
ollama serve
ollama pull gemma3:1b
ollama pull qwen3:1.7b
ollama run gemma3:1b
ollama list
```

---

## Minimal Python Check

```python
import json
import urllib.request

payload = {
    "model": "gemma3:1b",
    "prompt": "Write one line about data privacy.",
    "stream": False,
}

request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)

with urllib.request.urlopen(request, timeout=60) as response:
    data = json.loads(response.read().decode("utf-8"))

print(data["response"])
```

---

## Ollama Cloud Reference

If you want to try larger models without downloading them locally, Ollama Cloud requires authentication and uses a similar CLI workflow.

### Useful Links

- [Three ways in which Ollama makes trying new models much easier now](https://medium.com/@pandeyparul/three-ways-in-which-ollama-makes-trying-new-models-much-easier-now-a089d0ec18f7?sk=0bd54aefc221b0b55dd3072e2b20ce98)
