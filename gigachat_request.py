import json
import requests
import os

API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

def main():
    api_key = os.getenv("GIGACHAT_API_KEY")
    if not api_key:
        raise Exception("GIGACHAT_API_KEY not set in secrets")

    messages = [{"role": "user", "content": "Привет, кто ты?"}]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "GigaChat-2-Max",
        "scope": "GIGACHAT_API_CORP",
        "messages": messages,
        "max_tokens": 512
    }

    print("🚀 Отправляю запрос к GigaChat...")
    r = requests.post(API_URL, headers=headers, json=payload, verify=False)
    print("✅ Ответ получен:", r.status_code)

    # Сохраняем ответ в файл для публикации
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(r.json(), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
