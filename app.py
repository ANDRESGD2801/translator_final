from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen (necesario si abres el HTML directo)

# ── Cargar modelo Qwen2-0.5B ──────────────────────────────────────────────────
MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"
print(f"Cargando modelo {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="cpu",
)
model.eval()
print("Modelo listo.")


def translate_en_to_fr(text: str) -> str:
    """Traduce texto del inglés al francés usando Qwen2-0.5B."""
    prompt = (
        "Translate the following English sentence to French. "
        "Reply with ONLY the French translation, nothing else.\n\n"
        f"English: {text}\n"
        "French:"
    )

    messages = [
        {"role": "system", "content": "You are a professional translator. Translate English to French accurately."},
        {"role": "user",   "content": prompt},
    ]

    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer([text_input], return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,
            temperature=None,
            top_p=None,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decodificar solo los tokens generados (sin el prompt)
    generated = outputs[0][inputs["input_ids"].shape[1]:]
    result = tokenizer.decode(generated, skip_special_tokens=True).strip()

    # Limpiar posibles prefijos residuales
    for prefix in ("French:", "Translation:", "FR:"):
        if result.startswith(prefix):
            result = result[len(prefix):].strip()

    return result


# ── Rutas ──────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translation = translate_en_to_fr(text)
        return jsonify({"original": text, "translation": translation, "from": "English", "to": "French"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
