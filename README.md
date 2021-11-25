# ПРОЕКТ FOODGRAM [![Django-app workflow](https://github.com/eagurin/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/eagurin/foodgram-project-react/actions/workflows/main.yml)

## Ссылка на проект
http://51.250.5.216

# Установка Docker
Установите docker на сервер:
```
sudo apt install docker.io 
```

Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопируйте папки `docs` и `infra` на сервер в `~/`:



## Установка переменных окружения
Для работы с базой данных:
```sh
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнер в котором будет развернута БД)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=... # секретный ключ
DEBUG = True # данную опцию следует добавить для отладки
```

## Запуск приложения в Docker 
```sh
sudo docker-compose up -d  # Запустите docker-compose
sudo docker-compose exec -T backend python manage.py makemigrations  # Создать миграции миграции
sudo docker-compose exec -T backend python manage.py migrate --noinput  # Применить миграции
sudo docker-compose exec -T backend python manage.py collectstatic --no-input  # Собрать статику
sudo docker-compose exec -T backend python manage.py createsuperuser  # Создать суперпользователя
```

## Тестирование и работа API 
Для локального тестирования можно загрузить начальные данные
```
sudo docker-compose exec -T backend python manage.py loaddata dump.json
```
### Документация по API
http://51.250.5.216/api/docs/redoc.html

### Вход в админ-панель
http://51.250.5.216/admin
 
 
## В разработке использованы
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Gunicorn](https://gunicorn.org/)
* [Nginx](https://nginx.org/)
