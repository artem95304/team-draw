# Team Draw

Сервис для распределения участников по командам и парам.

## Запуск

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m uvicorn app_final:app
```

## Проверка

```bash
python -m pytest -v
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
```

Ожидаемые ответы: `{"status":"ok"}` и `{"version":"0.1.0"}`.

`APP_VERSION` задаёт версию приложения. По умолчанию — `0.1.0`.

## Логика приложения

- `POST /participants` — добавить участников. `text` содержит имя или список имён;
- `split_by_spaces=true` разделяет ввод по пробелам, `false` сохраняет полное имя целиком.
- `GET /participants` — посмотреть список.
- `DELETE /participants` — очистить список.

Каждый участник получает UUID и ник с номером: `Саша 1`, `Саша 2`.
Список хранится в памяти и очищается при перезапуске сервера.

После добавления участников вызовите `POST /draw/teams` в Swagger.
Параметр `team_count` задаёт число команд: от 1 до количества участников.
