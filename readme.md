# YaCut - сервис укорачивания ссылок

YaCut ассоциирует длинную ссылку с короткой: пользователь может предложить свой
вариант или получить сгенерированный сервисом. Дополнительно можно загрузить
сразу несколько файлов на Яндекс Диск и получить короткие ссылки на их скачивание
(загрузка асинхронная, через aiohttp).

Возможности:
- главная страница `/` - создание коротких ссылок;
- страница `/files` - загрузка файлов и генерация коротких ссылок к ним;
- переход по короткой ссылке ведёт на оригинальный адрес или скачивание файла;
- API с двумя эндпоинтами (см. `openapi.yml`).

## Технологии

- Python 3.12
- Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- aiohttp (асинхронные запросы к API Яндекс Диска)
- SQLite

## Запуск проекта

Клонировать репозиторий и перейти в него:

```
git clone git@github.com:Stepan-Pimenov/async-yacut.git
cd async-yacut
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

- Linux/macOS: `source venv/bin/activate`
- Windows: `source venv/Scripts/activate`

Установить зависимости:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создать файл `.env` (пример - в `.env.example`):

```
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///yacut.db
SECRET_KEY=ваш_секретный_ключ
DISK_TOKEN=ваш_токен_яндекс_диска
```

Токен Яндекс Диска получают на https://oauth.yandex.ru с доступами
`cloud_api:disk.app_folder` и `cloud_api:disk.info`.

Применить миграции и запустить проект:

```
flask db upgrade
flask run
```

## API

Спецификация - в файле `openapi.yml` (можно открыть в https://editor.swagger.io).

Создание короткой ссылки:

```
POST /api/id/
{
  "url": "https://practicum.yandex.ru/",
  "custom_id": "practicum"
}
```

Получение оригинальной ссылки по идентификатору:

```
GET /api/id/<short>/
```

## Автор

Степан Пименов - [github.com/Stepan-Pimenov](https://github.com/Stepan-Pimenov)
