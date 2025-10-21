import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    api_key = data.get("apiKey")
    messages = data.get("messages", [])
    system_prompt = data.get("systemPrompt", "You are a helpful assistant.")
    context = data.get("context", "")

    # Подготовим промпт
    full_prompt = system_prompt + ("\n\n" + context if context else "")

    # Формируем запрос к GigaChat API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "GigaChat-2-Max",
        "scope": "GIGACHAT_API_CORP",
        "messages": [{"role": "system", "content": full_prompt}, *messages],
        "max_tokens": 2048
    }

    try:
        # verify=False отключает проверку сертификата
        r = requests.post(
            "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
            headers=headers,
            json=payload,
            verify=False
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
