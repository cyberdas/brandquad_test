from django.db import models

# Поля модели должны содержать минимум: IP адрес, Дата из лога, http метод (GET, POST,...), 
# URI запроса, Код ответов, Размер ответа. Другие данные из лога - опциональны.
class Log(models.Model):

    ip_adress = models.GenericIPAddressField("Request IP adress")
    #date
    #http_method
    #request_uri
    #response_status_code
    #content_legth
    # user_agent
    # refer

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        pass
