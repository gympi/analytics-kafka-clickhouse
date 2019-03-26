import datetime
import inspect
import traceback
import uuid

from urllib.parse import urlparse

from libs.storage_adapters import kielKafkaAdapter
from .base import Base


state = {
    'open': 0,
    'close': 1,
}


vars_camelcase_to_snake_case = {
    'project': 'project',
    'path': 'path',
    'user_agent': 'userAgent',
    'url_visit': 'urlVisit',

    'timezone_client': 'timezoneClient',

    'state': 'state',
    'uid_client': 'analyticUidClient',

    'session_uid_client': 'sessionUidClient',
    'session_start_client': 'sessionStartClient',
    'session_duration_client': 'sessionDurationClient',
    'session_stop_client': 'sessionStopClient',

    'screen_width': 'screenWidth',
    'screen_height': 'screenHeight',

    'width': 'width',
    'height': 'height',
}


class TickHandler(Base):
    async def get(self):
        # print('TickHandler')
        # print(self.request.arguments)
        # print(len(self.request.cookies))
        # print(self.get_cookie('analytic_uid'))
        params = self._build_event()
        print(params)

        try:
            adapter = kielKafkaAdapter()
            adapter.send(params)
        except Exception as e:
            print("Error {}: ".format(inspect.currentframe().f_code.co_name), e)
            traceback.print_exc()

        self.on_write_json({'status': 'OK!', 'datetime': datetime.datetime.today(), 'sessionUidClient': params['session_uid_client']})

    def _build_event(self):
        url_visit = urlparse(self.get_argument('url_visit', ''))

        ver_uid_client, uid_client, timestamp_uid_client = self.get_cookie('analytic_uid').split('.')

        return {
            'timestamp': datetime.datetime.today().strftime("%s"),
            'request_ip': self.request.headers.get("X-Real-IP").strip() if self.request.headers.get(
                "X-Real-IP") else self.request.remote_ip.strip(),

            'project': url_visit.hostname,
            'path': url_visit.path + ('?' + url_visit.query) if url_visit.query else '',

            'user_agent': self.request.headers.get('User-Agent', ''),
            'timezone_client': self.get_argument('timezoneClient'),

            'state': self.get_argument('state') if self.get_argument('state') in state else state['open'],

            'ver_uid_client': ver_uid_client,
            'uid_client': uid_client,
            'timestamp_uid_client': timestamp_uid_client,

            'session_uid_client': self.get_argument('sessionUidClient', str(uuid.uuid4().hex)),

            'session_start_client': self.get_argument('sessionStartClient', 0),
            'session_duration_client': self.get_argument('sessionDurationClient', 0),
            'session_stop_client': self.get_argument('sessionStopClient', 0),

            'screen_width': self.get_argument('screenWidth', 0),
            'screen_height': self.get_argument('screenHeight', 0),

            'width': self.get_argument('width', 0),
            'height': self.get_argument('height', 0),
        }
