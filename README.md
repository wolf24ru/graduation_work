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
Для упрощенной проверки можно импортировать файл `Shop.postman_collection.json` в [Postman](https://www.postman.com/)
## Регистрация и авторизация пользователя:
___
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
## Города и Регионы:
___
### Получить список городов и регионов
**URL:** http//12.0.0.1:8000/api/v1/location/location_inform  
**METED:** GET  
**JSON EXAMPLE:**
```json
{
  "search_for": "city",
  "search": "Железногорск"
}
```
***
## Информация о магазинах:
___
### Вывод дейсвующих магазинов
**URL:** http//12.0.0.1:8000/api/v1/accounts/shops/  
**METED:** GET
***

### Получение статуса магазина
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
## Работа с товарами:
___
### Получить все категории товаров
**URL:** http//12.0.0.1:8000/api/v1/category/category/  
**METED:** GET
***


### Добваить до 3х продуктиов вручную
**URL:** http//12.0.0.1:8000/api/v1/product/add_products/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST   
**JSON EXAMPLE:**

```json
{
    "shop": 5,
    "products": [
        {
            "product": {
                "name": "Парат",
                "category": "Тумбочка"
            },
            "product_parameters":[
                {
                    "parameter":"Размер (ШхВхГ)",
                    "value": "60х50х50 см"
                },
                {
                   "parameter":"Цвет",
                    "value": "фиолетовый" 
                },
                {
                   "parameter":"Материал",
                    "value": "СДП" 
                }
                 ],
            "price": 7000,
            "quantity": 26,
            "img": "https://pm.ru/global_images/goods/31f/e37/c4c/4b6/1282586_preview.jpg",
            "external_id": 264515
        }
        ]
}
```
### Полное обнавлене каталога
**URL:** http//12.0.0.1:8000/api/v1/product/update_catalog/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST   
**JSON EXAMPLE:**

```json
{
   "url":"https://raw.githubusercontent.com/wolf24ru/graduation_work/main/yaml_files/shope1.yaml"
}
```
### Получить список информации о продуктах
**URL:** http//12.0.0.1:8000/api/v1/product/product_inform/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** GET  
не  обязательный **JSON EXAMPLE:**

```json
  {
  "query_params": {
    "shop_id": 2,
    "category_id": 1
  }
}
```
***
## Работа с заказами:
___
### Получить информацию о товарах в корзине
**URL:** http//12.0.0.1:8000/api/v1/order/basket/
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** GET  
**JSON EXAMPLE:**

### Создать новую карзину 
**URL:** http//12.0.0.1:8000/api/v1/order/basket/
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** POST  
**JSON EXAMPLE:**

```json
{
  "items":
  [
    {
    "order": "",
    "product_info": 3,
    "quantity": 3,
    },
    {
    "order": "",
    "product_info": 5,
    "quantity": 10
    }
  ] 
}
```

### Удаление продуктов из корзины
**URL:** http//12.0.0.1:8000/api/v1/order/basket/
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** DELETE  
**JSON EXAMPLE:**

```json
{
  "items": "1, 2"
}
```
###  Добавить продукты в карзину 
**URL:** http//12.0.0.1:8000/api/v1/order/basket/
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** PUT  
**JSON EXAMPLE:**

```json
{
  "items":
  [
    {
      "id": 10,
      "quantity": 10
    }
  ] 
}
```
***
###  Выдача списка заказов (для магазина) 
**URL:** http//12.0.0.1:8000/api/v1/order/vendor/   
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** GET
***
###  Получить список сделанных заказов (для пользователя)
**URL:** http//12.0.0.1:8000/api/v1/order/get/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** GET

### Создать заказ(переместить из корзины на исполнение)
**URL:** http//12.0.0.1:8000/api/v1/order/get/  
**HEADERS:** `Authorization Token b6c64b1e71a7770b94c49c9baf8f3e0b45872d5e`   
**METED:** PUT  
**JSON EXAMPLE:**
```json
{
  "contact": 4
}
```
contact - id_contact


