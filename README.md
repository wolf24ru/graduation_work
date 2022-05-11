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
```

### Запуск Doker

```shell
  docker-compose up -d --build
```

# Запросы:
## Регистрация и авторизация пользователя:
***
### Регистрация нового пользователя
**URL:** http//12.0.0.1:8000/api/v1/accounts/registration/  
**METED:** POST   
**JSON EXAMPLE:**

```json
{
  "first_name": "Имя",
  "last_name": "Фамилия",
  "email": "email@mail.ru",
  "password": "12345678qwerty",
  "company": "my compony",
  "position": "Мененджер",
  "username": "vany1",
  "type": "shop"
}
```
#### NOTE! Поле `type` не обязательно к заполнению для покупателя


***
### Получения Token
**URL:** http//12.0.0.1:8000/api-token-auth/  
**METED:** POST   
**JSON EXAMPLE:**
```json
{
  "username": "sflnjk@admin.ru",
  "password":"12345678qwerty"
}
```
### Получения нового Token
**URL:** http//12.0.0.1:8000/api/v1/accounts/new_token/  
**METED:** POST   
**HEADERS:** `Authorization Basic username:password`
***
### Вывод информации  пользователя
**URL:** http//12.0.0.1:8000/api/v1/accounts/user_filling/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`  
**METED:** GET  

### Изменение информации пользователя
**URL:** http//12.0.0.1:8000/api/v1/accounts/user_filling/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST   
**JSON EXAMPLE:**

```json
{
  "first_name": "Имя",
  "last_name": "Фамилия",
  "email": "email@mail.ru",
  "password": "12345678qwerty",
  "company": "my compony",
  "position": "Мененджер",
  "username": "vany1",
  "type": "buyer"
}
```
***
### Вывод дейсвующих магазинов
**URL:** http//12.0.0.1:8000/api/v1/accounts/shops/  
**METED:** GET
***

### Полдучение статуса магазина
#### Статус магазина - покуазывает может ли магазин принемать заказы илинет.
#### Досутпно только для пользователей с `type = shop`
**URL:** http//12.0.0.1:8000/api/v1/accounts/shop/order_accepting/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`  
**METED:** GET

### Изменение статуса магазина
**URL:** http//12.0.0.1:8000/api/v1/accounts/shop/order_accepting/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST   
**JSON EXAMPLE:**

```json
{
"order_accepting":"true"
}
```
***
### Получить всё контакты
**URL:** http//12.0.0.1:8000/api/v1/accounts/contacts/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** GET

### Добавить новый контакт
**URL:** http//12.0.0.1:8000/api/v1/accounts/contacts/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST   
**JSON EXAMPLE:**

```json
{
   "region":"Красноярский край",
   "city":"Красноярск",
   "street": "Мира",
   "house": "10",
   "structure": "3",
   "building": "2/5",
   "apartment":"254",
   "phone_number": "+7 (999) 123-32-44"
}
```

### Удалить контакты 
**URL:** http//12.0.0.1:8000/api/v1/accounts/contacts/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** DELETE   
**JSON EXAMPLE:**

```json
{
   "contacts_id":["5", "2"]
}
```
### Редактирование контакта
**URL:** http//12.0.0.1:8000/api/v1/accounts/contacts/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** PUT   
**JSON EXAMPLE:**

```json
{
  "id": 4,
  "region": "Красноярский край",
  "city": "Красноярск",
  "street": "Академика Павлова",
  "house": "150",
  "structure": "9",
  "building": "85",
  "apartment": "20",
  "phone_number": "89993154512"
}
```
***

