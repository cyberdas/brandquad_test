import time
from collections import defaultdict

from apachelogs import LogParser
from logging import getLogger

from logs.models import Log
# from logs.models import Log
# from logs.model import Log
# combined parser
# parser = LogParser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"')

# сначала работает без ThreadPoolExecutor
logger = getLogger(__name__)


class BulkCreateManager:
    def __init__(self, chunk_size=4000):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        try:
            model_class.objects.bulk_create(self._create_queues[model_key])
        except Exception as e:
            logger.error(f"Something went wrong while save to DB {e}")
            raise
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


class ApacheLogParser:
    """
    Класс ответственный за парсинг данных и сохранение в БД
    """
    def __init__(self):
        self.parser = LogParser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{Data}i\"')

    def parse_all(self, file_path: str):
        t1 = time.time()
        logger.info("Starting saving file to db")
        with open(file_path, 'r') as f:
            next(f)
            count = 0 # add http method, path
            bulk_mng = BulkCreateManager()
            for entry in self.parser.parse_lines(f, ignore_invalid=True):
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
            print(time.time() - t1)
                #a = line
                #print(line)
                #print(a)
                #entry = self.parser.parse(line)
                #print(entry)

if __name__ == '__main__':
    parser = ApacheLogParser()
    parser.parse_all(r'D:\Dev\brandquad_test\apachelogservice\logs\logs_dir\access.log')
# D:\Dev\brandquad_test\apachelogservice\logs\logs_dir\access_4.log
# Bulk create is my new friend.
# If anyone has the same problem, don't insert rows one at a time. 
# Each create() call is one insert statement. Instead, add the objects to a list, 
# and then bulk_create(the_list).
# before docker start create manage.py createsuperuser
# error while saving log(....) to db
# chunk -
# когда chunk заполнился - bulk_create
# обнуляем chunk