# graduation_work

## Выпускная работа
   

### Config file
Необходимо создать файл config со следующим содержанием, откорректировав под свою систему.  
```python
db_name = 'market_db' # название БД
db_user = 'market'  # Имя пользователя
db_password = '12345678'  # пароль
db_host = 'localhost'  # хост
db_port = '5430'  # порт БД на doker

EMAIL_HOST_USER = 'email@live.ru' # email
EMAIL_HOST_PASSWORD = 'qwerty1234' # пароль от email
```

### Запуск Doker

```shell
  docker-compose up -d --build
```

Для запуска необходимо:
1) ```sh
   python manage.py makemigrations
   ```
2) ```shell
    python manage.py migrate
    ```
3) ```shell
    python manage.py loaddata fixtures/fixture.json
    ```

Затем создать нового superusers:
```sh
python manage.py createsuperuser
```
