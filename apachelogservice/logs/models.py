from django.db import models


class Log(models.Model):
    """
    Поля модели должны содержать минимум: IP адрес, Дата из лога, http метод (GET, POST,...), 
    URI запроса, Код ответов, Размер ответа. Другие данные из лога - опциональны.
    """
    class HttpMethods(models.TextChoices):
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        PATCH = 'PATCH'
        DELETE = 'DELETE'
        HEAD = 'HEAD'
        OPTIONS = 'OPTIONS'
        CONNECT = 'CONNECT'
        TRACE = 'TRACE'
        DEFAULT = 'DEFAULT'
    ip_address = models.GenericIPAddressField('IP адрес запроса')
    timestamp = models.DateTimeField('Дата и время запроса')
    http_method = models.CharField(
        'HTTP Метод', max_length=7, choices=HttpMethods.choices, 
        default=HttpMethods.DEFAULT)
    request_path = models.CharField('Адрес запроса', max_length=200)
    http_protocol = models.CharField('HTTP протокол', max_length=10)
    response_status_code = models.PositiveIntegerField('Статус ответа сервера')
    content_length = models.PositiveIntegerField('Размер объекта', null=True, blank=True)
    referer = models.URLField('URL исходной страницы', null=True, blank=True) 
    user_agent = models.TextField('Клиентское приложение', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return f'{self.ip_address} [{self.timestamp}] ' \
               f'"{self.http_method} {self.request_path}" \
               {self.response_status_code} {self.content_length}'
