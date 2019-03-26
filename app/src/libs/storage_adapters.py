import json
from abc import ABC, abstractmethod
from clickhouse_driver import Client
from kafka import KafkaProducer
from kiel import clients
from libs.system_environment import SystemEnvironment


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


class kielKafkaAdapter(AnalyticsAdapter):
    def __init__(self):
        conf = SystemEnvironment().env['kafka']

        self._producer = clients.Producer(
            ['{}:{}'.format(conf['host'], conf['port'])],
            key_maker=None,
            partitioner=None,
            compression=None,
            batch_size=1,
            required_acks=1,
            ack_timeout=2000,  # milliseconds
        )

    def send(self, params):
        self._producer.produce('visit_stat_topic', params)
    # await self._producer.flush()




# from aiokafka import AIOKafkaProducer
# import asyncio
# import tornado.ioloop
# loop = asyncio.get_event_loop()
# # loop = tornado.ioloop.IOLoop.current()
# conf = SystemEnvironment().env['kafka']
# producer = AIOKafkaProducer(loop=loop, bootstrap_servers='{}:{}'.format(conf['host'], conf['port']),
#                                           value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))
#
# class AsyncKafkaAdapter:
#     def __init__(self):
#
#
#         # Get cluster layout and initial topic/partition leadership information
#         producer.start()
#
#     async def send(self, params):
#         try:
#             # Produce message
#             await producer.send_and_wait('visit_stat_topic', params)
#             await producer.flush()
#         finally:
#             pass
#
#             # Wait for all pending messages to be delivered or expire.
#             # await self._producer.stop()
