from django.db import models

# Create your models here.
# Поля модели должны содержать минимум: IP адрес, Дата из лога, http метод (GET, POST,...), 
# URI запроса, Код ответов, Размер ответа. Другие данные из лога - опциональны.
class Log(models.Model):

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        pass
