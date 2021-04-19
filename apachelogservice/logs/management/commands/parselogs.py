import os

from django.core.management.base import BaseCommand

from . import GivenUrlValidator, DownloadFile, ApacheLogParser


class Command(BaseCommand):
    """
    Management command for downloading, parsing and saving logs to db
    python manage.py parselogs --help
    """

    help = ('this command allows you to download logs from url, parse them and save to database, '
            'all log files are located at /apachelogservice/logs/log_dir')

    def add_arguments(self, parser):
        parser.add_argument('url', type=str,  help='url with logs')
        parser.add_argument('--delete', action='store_true', help='delete log file after loading')

    def handle(self, *args, **options):
        passed_url = options.get('url')
        url = self.validate_url(passed_url)
        file_path, time = self.download_file(url)
        self.stdout.write(self.style.SUCCESS(f'\nFile Downloaded Successfully, location: {file_path} \n'))
        self.stdout.write(self.style.SUCCESS(f'It took {time} seconds'))
        self.parse_and_load_to_db(file_path)
        self.stdout.write('Saved log data to DB')
        if options.get('delete'):
            os.remove(file_path)
            self.stdout.write('Deleted log file')

    def validate_url(self, passed_url: str):
        validator = GivenUrlValidator()  # валидация url
        valid_url = validator(passed_url)
        return valid_url

    def download_file(self, passed_url: str):
        downloader = DownloadFile()   # скачивание файла
        file_path, time = downloader(passed_url)
        return file_path, time

    def parse_and_load_to_db(self, file_path: str):
        parser = ApacheLogParser() # парсинг и сохранение в бд
        parser.parse_all(file_path)
