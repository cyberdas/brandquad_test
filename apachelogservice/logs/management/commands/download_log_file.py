import os
import requests
import time
import wget
from urllib.error import HTTPError

from django.core.management.base import CommandError
# дойдем до директории с логами
# получим имя файла по урлу, если он есть в директории, сгенериум новое имя файла
# имя файла используем c with open


class DownloadFile:
    """
    Класс для скачивания и создания log файла в директорию /logs_dir
    """
    def __init__(self):  #apachelogservice/
        self.save_path = os.path.join(os.getcwd(), 'logs/logs_dir')

    def generate_file_path(self, filename: str, file_path: str) -> str:
        """
        Если файл с таким названием существуем - добавляем цифру в конец названия
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
        filename = url.split('/')[-1] # получаем имя файла из url
        file_path = os.path.join(self.save_path, filename)
        if os.path.exists(file_path):
            file_path = self.generate_file_path(filename, file_path)
        return file_path

    def download_file(self, url: str, file_path: str):
        start_time = time.time()
        try:
            wget.download(url, out=file_path)
        except HTTPError:
            raise CommandError('HTTP Error 404: Not Found')
        # если файл с поменткой .tmp - удалить
        end_time = time.time() - start_time
        return end_time

    def __call__(self, url: str):
        file_path = self.get_file_path(url)
        # print(file_path)
        time = self.download_file(url, file_path)
        return file_path, time


if __name__ == "__main__":
    a = DownloadFile()
    a('http://www.almhuette-raith.at/apache-log/access.log')
# http://www.almhuette-raith.at/apache-log/access.log D:\\Dev\\brandquad_test\\apachelogservice/logs/logs_dir\\access.log
# https://www.youtube.com/watch?v=3ndEeGDVqD4 'D:\\Dev\\brandquad_test\\apachelogservice/logs/logs_dir\\watch?v=3ndEeGDVqD4'
# https://docs.python.org/3/library/shutil.html