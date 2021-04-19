import os
import time
import wget

from logging import getLogger
from urllib.error import HTTPError

from django.core.management.base import CommandError


logger = getLogger(__name__)


class DownloadFile:
    """
    Класс для скачивания и создания log файла в директорию /logs_dir
    """
    def __init__(self):
        self.save_path = os.path.join(os.getcwd(), 'logs', 'logs_dir')

    def generate_file_path(self, filename: str, file_path: str) -> str:
        """
        Если файл с таким названием существует - добавляем цифру в конец названия
        """
        new_file_path = file_path
        root, ext = os.path.splitext(filename)
        i = 0
        while os.path.exists(new_file_path):
            i += 1
            new_filename = '%s_%i%s' % (root, i, ext)
            new_file_path = os.path.join(self.save_path, new_filename)
        return new_file_path

    def get_file_path(self, url: str):
        """
        Получаем имя файла и путь
        """
        filename = url.split('/')[-1]
        file_path = os.path.join(self.save_path, filename)
        if os.path.exists(file_path):
            file_path = self.generate_file_path(filename, file_path)
        return file_path

    def download_file(self, url: str, file_path: str):
        """
        Скачиваем файл и удаляем temp файл при ошибке
        """
        start_time = time.time()
        logger.info('Downloading file')
        try:
            wget.download(url, out=file_path)
        except HTTPError:
            raise CommandError('HTTP Error 404: Not Found')
        except OSError as e:
            raise CommandError(f'Something went wrong, cant download log from url - {e}')
        finally:  # сталкивался с тем, что wget после работы оставлял .tmp file
            for item in os.listdir(self.save_path):
                if item.endswith('.tmp'):
                    os.remove(os.path.join(self.save_path, item))
        end_time = time.time() - start_time
        return end_time

    def __call__(self, url: str):
        file_path = self.get_file_path(url)
        time = self.download_file(url, file_path)
        return file_path, time
