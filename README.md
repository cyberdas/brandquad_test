# ApacheLogService
Django приложение, которое скачивает логи, парсит их и сохраняет в БД (хотел в качестве СУБД использовать POSTGRES, но в SQLite оказался быстрее)
Доступно по команде
```
python manage.py parselogs <ваш url>
```
Данные будут доступны для просмотра в интерфейсе администратора - 127.0.0.1/admin
## Запустить проект
1) Клонируйте репозиторий 
```
git clone https://github.com/cyberdas/brandquad_test.git
```
2) В директории apachelogsservice создайте файл .env с переменным окружения (в качестве примера можно использовать эти)
- POSGRES_DB=logs
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432
## Запустить проект с помощью Docker
3) Разверните проект с помощью docker-compose
```
docker-compose up --build
```
4) Выполните миграции, создайте суперпользователя, соберите статику:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```
