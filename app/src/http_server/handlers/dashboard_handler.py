import copy

from libs.clickhouse_connect import session
from libs.entities import VisitStat
from http_server.handlers.base import Base


class DashboardHandler(Base):
    _template_file = 'dashboard.html'

    _default_params = {
        'page': 1,
        'limit': 10
    }

    def get(self):
        params = copy.copy(self._default_params)

        for k, v in params.items():
            if v is None:
                _type = str
            else:
                _type = type(v)

            try:
                params[k] = _type(self.get_argument(k, v))
            except Exception:
                params[k] = self.get_argument(k, v)

        offset = params['limit'] * (params['page'] - 1)
        query = session().query(VisitStat)

        self.on_write_page(template=self._template_file,
                           params={'title': 'Analytics Dashboard',
                                   'cols': VisitStat.__table__.columns.keys(),
                                   'items': query.order_by(VisitStat.timestamp.desc()).limit(params['limit']).offset(offset).all(),
                                   'count': int(query.count()),
                                   'offset': offset,
                                   **params})
