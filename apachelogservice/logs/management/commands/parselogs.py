import os

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.management.base import BaseCommand, CommandError

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
        validator = GivenUrlValidator()
        validator(passed_url)
        downloader = DownloadFile()
        file_path, time = downloader(passed_url)
        self.stdout.write(self.style.SUCCESS(f'\nFile Downloaded Successfully, location: {file_path} \n'))
        self.stdout.write(self.style.SUCCESS(f'It took {time} seconds'))
        parser = ApacheLogParser()
        parser.parse_all(file_path)
        self.stdout.write('Saved log data to DB')
        if options.get('delete'):
            os.remove(file_path)
            self.stdout.write('Deleted log file')
        #parser = ApacheLogParser()
        #parser.parse_all('D:\Dev\brandquad_test\apachelogservice\logs\logs_dir\access_4.log')
        #parser.parse_all(file_path)
        #self.stdout.write(self.style.SUCCESS(f'File {filepath} successfully parsed and saved to db')) 
        #try:
       #     d = DownLoadFile(url)  # скачиваем файл и сохраняем, название файла содержит текущую дату для избегания повторения
       # except:
       #     pass
       # else:
        #    self.stdout.write(self.style.SUCCESS("File Downloaded Successfully"))
        # download file
        # url = GivenUrlValidator(passed_url)
        #print(f'Command: {options["url"]}')
        #print('Second line')
        #if len(options['url']) > 3:
            #self.stdout.write(self.style.SUCCESS('We did it reddit'))
        #else:
            #raise CommandError("wrong url")
        #url = options['url']
        # print(url)
