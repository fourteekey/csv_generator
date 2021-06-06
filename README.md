### Установка проекта
```
$ pip install -r requirements
$ cd backend
$ cp config/example.env config/.env
$ nano config/.env
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py insert_technical_data
$ python manage.py createsuperuser
 ```


### Запуск бэкенда
``
Все действия происходят в папке backend
``
```
$ python manage.py runserver
```


