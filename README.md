# ApacheLogService
Django приложение, которое скачивает логи, парсит их и сохраняет в БД (хотел в качестве СУБД использовать POSTGRES, но SQLite оказался быстрее).
Логи скачиваются в директорию logs/logs_dir
# Команда:
```
python manage.py parselogs --help - информация о команде
```
Данные будут доступны для просмотра в интерфейсе администратора - 127.0.0.1/admin
## Запустить проект
1) Клонируйте репозиторий
```
git clone https://github.com/cyberdas/brandquad_test.git
```
## Запустить проект с помощью Docker
2) Разверните проект с помощью docker-compose
```
docker-compose up --build
```
3) Миграции, создайте суперпользователя, соберите статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```
