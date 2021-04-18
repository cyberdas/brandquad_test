# ApacheLogService
Django приложение, которое скачивает логи, парсит их и сохраняет в БД (хотел в качестве СУБД использовать POSTGRES, но SQLite оказался быстрее)
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
## Запустить проект с помощью Docker
3) Разверните проект с помощью docker-compose
```
docker-compose up --build
```
4) создайте суперпользователя, соберите статику:
```
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```
