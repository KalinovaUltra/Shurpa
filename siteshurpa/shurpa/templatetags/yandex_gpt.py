import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def ask_yandex_gpt(prompt, temperature=0.6):
    if not getattr(settings, 'YANDEX_CLOUD_API_KEY', None):
        logger.error("API ключ не настроен")
        return "Ошибка: API ключ не настроен"

    folder_id = getattr(settings, 'YANDEX_FOLDER_ID', None)
    if not folder_id or not folder_id.startswith('b1g'):
        logger.error(f"Неверный Folder ID: {folder_id}")
        return "Ошибка: Неверный формат Folder ID"

    # Corrected model URI
    model_uri = f"gpt://{folder_id}/yandexgpt-lite/latest"
    logger.info(f"Используем modelUri: {model_uri}")

    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_CLOUD_API_KEY}",
        "Content-Type": "application/json"  # x-folder-id is not needed in headers
    }

    payload = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": max(0.1, min(float(temperature), 1.0)),
            "maxTokens": 2000,  # Fixed value
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — помощник ресторана 'Шурпа'. Отвечай кратко и вежливо."
            },
            {
                "role": "user",
                "text": str(prompt)[:1000]
            }
        ]
    }

    try:
        response = requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers=headers,
            json=payload,
            timeout=15
        )
        if response.status_code == 404:
            logger.error(f"Модель не найдена. Проверьте: {model_uri}")
            return "Ошибка: Модель не активирована. Запустите: yc foundation-models activate --folder-id YOUR_FOLDER_ID --model-name yandexgpt-lite"

        response.raise_for_status()
        return response.json()["result"]["alternatives"][0]["message"]["text"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {str(e)}")
        return f"Ошибка API: {str(e)}"
    except KeyError as e:
        logger.error(f"Ошибка формата ответа: {str(e)}. Полный ответ: {response.text}")
        return "Ошибка: Неверный формат ответа от API"