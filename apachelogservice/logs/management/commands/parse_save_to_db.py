import time
import requests
import tqdm
from collections import defaultdict

from apachelogs import LogParser
from django.apps import apps
from logging import getLogger

from logs.models import Log


# logger = getLogger(__name__)

class BulkCreateManager:
    """
    Когда количество добавленных в очередь объектов превышает chunk_size,
    они добавляются в БД
    """
    def __init__(self, chunk_size=4000):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        try:
            model_class.objects.bulk_create(self._create_queues[model_key])
        except Exception as e:
            logger.error(f'Something went wrong while save to DB {e}')
            raise
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Добавить объект в очередь для добавления
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


class ApacheLogParser:
    """
    Класс ответственный за парсинг и сохранение логов в БД
    Скачивание происходит итеративно и без сохранения на диск
    """
    def __init__(self):
        self.parser = LogParser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{Data}i\"')

    def test(self, url):
        bulk_mng = BulkCreateManager()
        with requests.get(url, stream=True) as r: # итеруемся по объекту ответа
            # content_length = 66246212
            # r.raise_for_status()
            # chunk_size - байты
            # for line in generator
            for line in r.iter_lines(decode_unicode=True): # загружаем ответ в память не целиком
                if line:
                    entry = self.parser.parse(line)
                    ip_address = entry.remote_host
                    timestamp = entry.request_time
                    response_status_code = entry.final_status
                    http_method, request_path, http_protocol = entry.request_line.split()
                    content_length = entry.bytes_sent
                    user_agent = entry.headers_in['User-Agent']
                    referer = entry.headers_in['Referer']
                #for entry in self.parser.parse_lines(line, ignore_invalid=False):
                #    ip_address = entry.remote_host
                #    timestamp = entry.request_time
                #    response_status_code = entry.final_status
                #    http_method, request_path, http_protocol = entry.request_line.split()
                #    content_length = entry.bytes_sent
                #    user_agent = entry.headers_in['User-Agent']
                #    referer = entry.headers_in['Referer']
                    bulk_mng.add(Log(
                        ip_address=ip_address,
                        timestamp=timestamp,
                        response_status_code=response_status_code,
                        http_method=http_method,
                        request_path=request_path,
                        http_protocol=http_protocol,
                        content_length=content_length,
                        user_agent=user_agent,
                        referer=referer
                    ))
            bulk_mng.done()


    def parse_all(self, url: str):
        #logger.info()
        start_time = time.time()
        self.test(url)
        end_time = time.time()
        return end_time - start_time

#
# класс Bulk create manager добавить метод в модель?
# строка с процессов tqdm
# логировать could not parse line {}, it is not saved to db
# started parsing {url}
#

if __name__ == '__main__':
    a = ApacheLogParser()
    a.parse_all('http://www.almhuette-raith.at/apache-log/access.log')
