import datetime
import inspect
import traceback
import uuid

from urllib.parse import urlparse

from libs.storage_adapters import KafkaAdapter
from .base import Base


state = {
    'open': 0,
    'close': 1,
}


class TickHandler(Base):
    def get(self):
        print('TickHandler')
        print(self.request.arguments)
        print(len(self.request.cookies))
        print(self.get_cookie('analytic_uid'))
        params = self._build_event()
        print(params)

        try:
            adapter = KafkaAdapter()
            adapter.send(params)
        except Exception as e:
            print("Error {}: ".format(inspect.currentframe().f_code.co_name), e)
            traceback.print_exc()

        self.on_write_json({'status': 'OK!', 'datetime': datetime.datetime.today(), **params})

    def _build_event(self):
        url_visit = urlparse(self.get_argument('url_visit', ''))

        ver_user_uid, user_uid, timestamp_create_user_uid = tuple(self.get_cookie('analytic_uid').split('.'))

        return {
            # 'date_visit': datetime.date.today().strftime("%Y-%m-%d"),
            # 'time_visit': datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            'timestamp': datetime.datetime.today().strftime("%s"),
            'project': url_visit.hostname,
            'path': url_visit.path + ('?' + url_visit.query) if url_visit.query else '',

            'request_ip': self.request.headers.get("X-Real-IP").strip() if self.request.headers.get(
                "X-Real-IP") else self.request.remote_ip.strip(),
            'user_agent': self.request.headers.get('User-Agent', ''),
            'user_timezone': self.get_argument('timezone'),
            'user_timestamp':  self.get_argument('timestamp'),

            'user_cookie_ver':

            'state': self.get_argument('state') if self.get_argument('state') in state else state['open'],
            'analytic_uid': self.get_cookie('analytic_uid'),
            'page_session_uid': self.get_argument('page_session_uid', str(uuid.uuid4().hex))
        }
