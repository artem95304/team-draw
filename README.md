# Team Draw

## Назначение

Сервис жеребьёвки для организаторов игр и учебных занятий:
случайно распределяет участников по командам или парам.

## Установка

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Запуск

Обычный запуск:

```bash
python -m uvicorn app_final:app
```

Swagger: http://127.0.0.1:8000/docs

## Тесты

```bash
python -m pytest -v
```

## Переменные окружения

`APP_VERSION` — версия приложения, по умолчанию `0.1.0`.

## Проверка и логи

При запущенном сервере в другом терминале:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
```

Ответы по умолчанию: `{"status":"ok"}` и `{"version":"0.1.0"}`.
Логи выводятся в терминал, где запущен сервер.
