import os

from django.core.management.base import BaseCommand

from . import GivenUrlValidator, DownloadFile, ApacheLogParser


class Command(BaseCommand):
    """
    Вторая версия management команды для парсинга логов
    Файл с логами на скачивается, парсинг и сохранение в БД за один проход
    """

    help = ('this command allows you to download logs from url, parse them and save to database')

    def add_arguments(self, parser):
        parser.add_argument('url', type=str,  help='url with logs')

    def handle(self, *args, **options):
        passed_url = options.get('url')
        url = self.validate_url(passed_url)
        time = self.parse_and_load_to_db(url)
        print(time)
        self.stdout.write(self.style.SUCCESS(f'Saved logs to DB, it took {time} seconds'))

    def validate_url(self, passed_url: str) -> str:
        validator = GivenUrlValidator()  # валидация url
        valid_url = validator(passed_url)
        return valid_url

    def parse_and_load_to_db(self, url: str):
        parser = ApacheLogParser() # парсинг и сохранение в бд
        time = parser.parse_all(url)
        return time
