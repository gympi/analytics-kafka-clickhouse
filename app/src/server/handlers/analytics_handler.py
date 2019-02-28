import inspect
import json
import traceback

from app.src.server.handlers.base import Base
from clickhouse_driver import Client
from system_environment import SystemEnvironment
from urllib.parse import urlparse

from kafka import KafkaProducer

conf = SystemEnvironment().env['clickhouse']


class AnalyticsAdapter:
    def send(self, **kwargs):
        pass


class ClickhouseAdapter(AnalyticsAdapter):
    def __init__(self):
        self._client = Client(conf['host'])

    def send(self, params):
        sql = '''
        INSERT INTO `tvz_analytics`.`visit_stat`
            ({})
        VALUES '''.format(cols=','.join(list(map(lambda x: '`{}`'.format(x), params.keys()))))

        self._client.execute(sql, [params])


class KafkaAdapter(AnalyticsAdapter):
    def __init__(self):
        self._producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                       value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))

    def send(self, params):
        self._producer.send('topic', params)
        self._producer.flush()


adapters = {
    'clickhouse': ClickhouseAdapter,
    'kafka': KafkaAdapter
}


class AnalyticsHandler(Base):
    def get(self):
        try:
            params = self._build_event()
            adapter = adapters.get('kafka')()
            adapter.send(params)

            # print_data()

        except Exception as e:
            print("Error {}: ".format(inspect.currentframe().f_code.co_name), e)
            traceback.print_exc()
            exit()

        self.on_write_json({'status': 'OK!'})

    def _build_event(self):
        url_visit = urlparse(self.get_argument('url_visit', ''))

        return {
            'timestamp': 123,
            'level': '123',
            'message': self.request.headers.get('User-Agent', ''),

            # 'date_visit': date.today(),
            # 'time_visit': datetime.today(),
            # 'project': url_visit.hostname,
            # 'sub_project': '',
            # 'path': url_visit.path,
            # 'request_ip': self.request.headers.get("X-Real-IP").strip() if self.request.headers.get(
            #     "X-Real-IP") else self.request.remote_ip.strip(),
            # 'user_agent': self.request.headers.get('User-Agent', '')
        }
