# English → French Translator

A lightweight English-to-French translator built with two independent approaches: a **100% browser-based** version powered by Transformers.js, and a **local Python/Flask backend** powered by Qwen2.

---

## Two Implementations

### `index.html` — Browser-only (no Python, no API keys)

Opens directly in any modern browser. The translation model (`Xenova/opus-mt-en-fr`) is downloaded once from Hugging Face (~80 MB) and cached locally. After that, everything runs entirely on your device — no server, no internet connection needed.

**How to use:**
1. Open `index.html` in your browser.
2. Wait for the model to finish loading (progress bar shown on first visit).
3. Type any English text or pick one of the example chips.
4. Click **Translate** or press `Ctrl + Enter`.

**Tech stack:**
- [`@huggingface/transformers`](https://github.com/huggingface/transformers.js) v3 (via CDN)
- Model: `Xenova/opus-mt-en-fr` (MarianMT, optimized for browser)

---

### `app.py` — Flask backend (Python)

A REST API that uses the **Qwen2-0.5B-Instruct** language model running locally on CPU. The frontend sends a POST request to `/translate` and receives the French translation.

**Requirements:**
```
pip install flask flask-cors transformers torch
```

**How to run:**
```bash
python app.py
```

The server starts at `http://localhost:5000`. Open `index.html` or send requests directly:

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'
```

**Response:**
```json
{
  "original": "Hello, how are you?",
  "translation": "Bonjour, comment allez-vous ?",
  "from": "English",
  "to": "French"
}
```

**Tech stack:**
- [Flask](https://flask.palletsprojects.com/) + [flask-cors](https://flask-cors.readthedocs.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- Model: [`Qwen/Qwen2-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct) (runs on CPU)

---

## Quick Comparison

| | `index.html` | `app.py` |
|---|---|---|
| Setup | None (open in browser) | `pip install` + `python app.py` |
| Model | opus-mt-en-fr (MarianMT) | Qwen2-0.5B-Instruct |
| Runs on | Browser (WASM) | Python / CPU |
| Internet needed | First load only | First load only |
| API key | No | No |
