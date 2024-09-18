<h1 align="center">Справочник терминологии</h1>
<h1 align="center">Развертывание проекта</h1>

<h2>Скачать проект</h2>

```
  git clone https://github.com/A-V-tor/terminology-service.git
```

```
  cd terminology-service
```

### Создать виртуальное окружение и установить зависимости

```
  python -m venv venv
```
```
  source venv/bin/activate
```
```
  pip install -r requirements.txt
```

или

```
  poetry shell
```
```
  poetry install
```
Создать файл `.env` по аналогии с `env.example`<br>

Создать и применить миграции
```
  python manage.py makemigrations
```

```
  python manage.py migrate
```

Создать сущность админа
```
  python manage.py createsuperuser
```

Наполнить базу данных записями

```
  python load_sql.py
```

#### Запуск сервера

```
  python manage.py runserver
```

Роуты:<br>
Swagger документация http://127.0.0.1:8000/api/schema/swagger-ui/<br>
Админка http://127.0.0.1:8000/admin<br>
Список справочников http://127.0.0.1:8000/api/v1/refbooks/<br>

Элементы справочника с учетом версионирования http://127.0.0.1:8000/api/v1/refbooks/1/elements/?version=2.0<br>

Проверка элемента справочника http://127.0.0.1:8000/api/v1/refbooks/1/check_element/?code=1&value=%D0%92%D1%80%D0%B0%D1%87-%D1%82%D0%B5%D1%80%D0%B0%D0%BF%D0%B5%D0%B2%D1%82&version=1.0


### Запуск тестов

```
   pytest 
```
 
```
  pytest --cov
```


### Сборка через докер

```
  docker-compose build
```

```
  docker-compose up
```