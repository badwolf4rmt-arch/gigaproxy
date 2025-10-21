# gigachat_request.py
# Полностью автономный запрос к GigaChat API с автоматическим получением токена
import os
import json
import requests
import base64

# === Конфигурация ===
OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

def get_access_token():
    """Получает новый токен GigaChat с использованием client_id и client_secret"""
    client_id = os.getenv("GIGACHAT_CLIENT_ID")
    client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise Exception("❌ Client ID или Client Secret не заданы в секретах GitHub")

    # Кодируем client_id и client_secret в Base64 для Basic Auth
    creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    print("🔐 Получаю новый токен...")
    response = requests.post(
        OAUTH_URL,
        headers={"Authorization": f"Basic {creds}"},
        data={"scope": "GIGACHAT_API_CORP"},
        verify=False  # отключаем проверку сертификатов Минцифры
    )

    if response.status_code != 200:
        raise Exception(f"Ошибка при получении токена: {response.status_code} {response.text}")

    token = response.json().get("access_token")
    if not token:
        raise Exception("⚠️ Не удалось извлечь access_token из ответа")
    
    print("✅ Токен успешно получен")
    return token


def query_gigachat(prompt):
    """Отправляет сообщение в GigaChat"""
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "GigaChat-2-Max",
        "scope": "GIGACHAT_API_CORP",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }

    print(f"🚀 Отправляю запрос к GigaChat: {prompt[:50]}...")
    response = requests.post(API_URL, headers=headers, json=data, verify=False)

    print(f"🔍 Код ответа: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Ошибка при обращении к GigaChat: {response.text}")

    result = response.json()
    print("✅ Ответ успешно получен")
    return result


def main():
    """Основная функция — выполняет запрос и сохраняет результат"""
    try:
        result = query_gigachat("Привет! Кто ты?")
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("📄 Результат сохранён в result.json")
    except Exception as e:
        print("❌ Ошибка:", str(e))
        with open("result.json", "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
