# graduation_work

## Выпускная работа
   
Необходиомо создать ``.env`` файл виртаульного окружения
### .env file
```
POSTGRES_USER=market
POSTGRES_PASSWORD=12345678
POSTGRES_DB=market_db
POSTGRES_PORT=5432
POSTGRES_HOST=db

EMAIL_HOST_USER=email@live.ru
EMAIL_HOST_PASSWORD=qwerty1234
EMAIL_HOST_PORT=587
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_USE_TLS=True

SECRET_KEY=django-insecure-p@ku57h=!suz$&&%k^ykn%itg#qhhfeqvgg)jg_ix7&+(hn!_9
DEBUG=0

BROKER_URL=redis://cache:6379
CELERY_RESULT_BACKEND=redis://cache:6379
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_TIMEZONE=Asia/Krasnoyarsk

YANDEX_ID=
YANDEX_SECRET=

GOOGLE_ID=
GOOGLE_SECRET=

KV_ID=
VK_SECRET=
```
ID и SECRET можно взять в конкретных сервисах:  
* [Google](https://console.cloud.google.com/apis/credentials?project=my-test-shope)
* [VK](https://vk.com/editapp?act=create)
* [Yandex](https://oauth.yandex.com/client/new)

### Запуск Doker

```shell
  docker-compose up -d --build
```

# Запросы:
Для вывода всех возможных запросов можно посмотреть документацию:  
http://127.0.0.1:8000/api/schema/swagger-ui/
либо 
http://127.0.0.1:8000/api/schema/redoc/

Зарегистрироваться или авторизоваться можно через запрос который есть в приведенной выше документации,
а так же при помощи социальных сетей или заполнив форму перейдя по ссылке http://127.0.0.1:8000/accounts/login/

Для выхода из учетной записи перейти по ссылке http://127.0.0.1:8000/accounts/logout/