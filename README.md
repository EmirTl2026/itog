# «Currency Converter»
**Автор:** Тлеужев Эмир
**Вариант:** «Currency Converter»
**Дата сдачи:** 30.04.2026
## Описание программы
** «Currency Converter» - Приложение для конвертации валют с использованием внешнего API и сохранением истории.**
## Требования для запуска
- Python 3.10 или выше
- Библиотеки: 'pip install requests'
## Как получить API-ключ
1. Зарегистрируйтесь на exchangerate-api.com.
2. Получите ключ и вставьте его в переменную API_KEY в коде.
3. Использование внешнего API

Пример запроса:

import requests

API_KEY = "ВАШ_API_КЛЮЧ"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

def get_rate(from_cur, to_cur):
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}")
    data = response.json()
    return data["conversion_rate"]

## Примеры использования
1. Команда запуска `python main.py`
2. Выберите валюты, введите сумму и нажмите «Конвертировать».
3. История сохраняется в history.json.
