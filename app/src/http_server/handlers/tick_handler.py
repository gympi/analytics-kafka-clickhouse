import datetime
import inspect
import traceback

from urllib.parse import urlparse

from libs.storage_adapters import KafkaAdapter
from .base import Base


class TickHandler(Base):
    def get(self):
        try:
            print('TickHandler')
            print(self.request.arguments)
            print(len(self.request.cookies))
            print(self.get_cookie('analytic_uid'))
            params = self._build_event()
            adapter = KafkaAdapter()
            print(params)
            self.set_header('Access-Control-Allow-Origin', params['hostname'])

            adapter.send(params)

        except Exception as e:
            print("Error {}: ".format(inspect.currentframe().f_code.co_name), e)
            traceback.print_exc()

        self.on_write_json({'status': 'OK!', 'datetime': datetime.datetime.today()})

    def _build_event(self):
        url_visit = urlparse(self.get_argument('url_visit', ''))
        return {
            # 'date_visit': datetime.date.today().strftime("%Y-%m-%d"),
            # 'time_visit': datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            'timestamp': datetime.datetime.today().strftime("%s"),
            'project': url_visit.hostname,
            'path': url_visit.path + ('?' + url_visit.query) if url_visit.query else '',
            'request_ip': self.request.headers.get("X-Real-IP").strip() if self.request.headers.get(
                "X-Real-IP") else self.request.remote_ip.strip(),
            'user_agent': self.request.headers.get('User-Agent', '')
        }
