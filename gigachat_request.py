

import os, json, requests

# === ПОЛУЧАЕМ НОВЫЙ ТОКЕН ===
OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
client_id = os.getenv("GIGACHAT_CLIENT_ID")
client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")

print("🔐 Получаю новый access_token...")
r = requests.post(
    OAUTH_URL,
    headers={"Authorization": f"Basic {client_id}:{client_secret}"},
    data={"scope": "GIGACHAT_API_CORP"},
    verify=False
)
token = r.json().get("access_token")
if not token:
    raise Exception("❌ Не удалось получить токен: " + r.text)
print("✅ Токен получен!")

# === ОСНОВНОЙ ЗАПРОС ===
API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
payload = {
    "model": "GigaChat-2-Max",
    "scope": "GIGACHAT_API_CORP",
    "messages": [{"role": "user", "content": "Привет, кто ты?"}],
    "max_tokens": 512,
}

print("🚀 Отправляю запрос к GigaChat...")
r = requests.post(API_URL, headers=headers, json=payload, verify=False)
print("Ответ:", r.status_code, r.text)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(r.json(), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
