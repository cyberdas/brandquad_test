from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.management.base import BaseCommand, CommandError

from . import GivenUrlValidator, DownloadFile
# self.style.SUCCESS, WARNING, ERROR
# WARNING is yellow
#nargs=количество аргументов
class Command(BaseCommand):

    help = ('this command allows you to download logs from url, parse them and save to database, '
            'all log files are located /apachelogservice/logs/log_dir')

    def add_arguments(self, parser):
        parser.add_argument('url', type=str,  help='url with logs')
        # ignore errors?

    def handle(self, *args, **options):
        passed_url = options.get('url')
        # self.stdout.write(self.style.WARNING("123"))
        validator = GivenUrlValidator() # класс ответственный за валидацию
        validator(passed_url)
        downloader = DownloadFile()
        file_path, time = downloader(passed_url)
        self.stdout.write(self.style.SUCCESS(f'\nFile Downloaded Successfully, location:{file_path} \n'))
        self.stdout.write(self.style.SUCCESS(f'It took {time} time'))
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