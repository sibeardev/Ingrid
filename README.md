# Ingrid
Beauty salon web application

## Как запустить dev-версию сайта

Скачайте код:
```sh
git clone https://github.com/sibeardev/Ingrid.git
```

Перейдите в каталог проекта:
```sh
cd Ingrid
```

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение и активируйте его:
```sh
python -m venv .venv
```

- Windows: `.\.venv\Scripts\activate`
- MacOS/Linux: `source .venv/bin/activate`

Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создать файл `.env` в каталоге `Ingrid/` со следующим содержимым:
```sh
SECRET_KEY=<super-secret-code>
DEBUG=TRUE
```

Создайте файл базы данных SQLite:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
