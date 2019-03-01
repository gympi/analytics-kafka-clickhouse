import json
from abc import ABC, abstractmethod
from clickhouse_driver import Client
from kafka import KafkaProducer

from app.src.libs.system_environment import SystemEnvironment


class AnalyticsAdapter(ABC):
    @abstractmethod
    def send(self, params):
        pass


class ClickhouseAdapter(AnalyticsAdapter):
    def __init__(self):
        conf = SystemEnvironment().env['clickhouse']
        self._client = Client(conf['host'])

    def send(self, params):
        cols = ','.join(list(map(lambda x: '`{}`'.format(x), params.keys())))

        sql = '''
        INSERT INTO `analytics`.`visit_stat`
            ({})
        VALUES '''.format(cols)

        self._client.execute(sql, [params])


class KafkaAdapter(AnalyticsAdapter):
    def __init__(self):
        conf = SystemEnvironment().env['kafka']
        self._producer = KafkaProducer(bootstrap_servers='{}:{}'.format(conf['host'], conf['port']),
                                       value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))

    def send(self, params):
        self._producer.send('visit_stat_topic', params)
        self._producer.flush()
