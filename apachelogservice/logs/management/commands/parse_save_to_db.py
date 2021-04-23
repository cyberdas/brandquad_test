import time
import requests
import tqdm
from collections import defaultdict

from apachelogs import LogParser
from django.apps import apps
from logging import getLogger

# from logs.models import Log


# logger = getLogger(__name__)


class ApacheLogParser:
    """
    Класс ответственный за парсинг и сохранение логов в БД
    Скачивание происходит итеративно и без сохранения на диск
    """
    def __init__(self):
        self.parser = LogParser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{Data}i\"')

    def test(self, url):
        with requests.get(url, stream=True) as r: # итеруемся по объекту ответа
            # content_length = 66246212
            # r.raise_for_status()
            # iter_lines (chunk_size)
            for line in r.iter_lines(decode_unicode=False): # загружаем ответ в память не целиком
                for entry in self.parser.parse_lines(line, ignore_invalid=False):
                    ip_address = entry.remote_host
                    timestamp = entry.request_time
                    response_status_code = entry.final_status
                    http_method, request_path, http_protocol = entry.request_line.split()
                    content_length = entry.bytes_sent
                    user_agent = entry.headers_in['User-Agent']
                    referer = entry.headers_in['Referer']
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
