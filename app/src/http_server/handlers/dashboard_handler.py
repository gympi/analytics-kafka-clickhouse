import copy

from libs.clickhouse_connect import session
from libs.entities import VisitStat
from http_server.handlers.base import Base


class DashboardHandler(Base):
    _template_file = 'dashboard.html'

    _default_params = {
        'draw': 1,
        'page': 1,
        'limit': 10,
        'start': 10,
        'length': 10,
        'order': None
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

        params['page'] = params['draw']
        params['limit'] = params['length']

        offset = params['start']
        oder_col = self.get_argument('order[0][column]', None)
        oder_type = self.get_argument('order[0][dir]', None)

        query = session().query(VisitStat)

        if oder_col:
            if oder_type == 'desc':
                cols = list(VisitStat.__table__.columns.keys())
                query = query.order_by(getattr(VisitStat, cols[int(oder_col)-1]).desc())
        else:
            query = query.order_by(VisitStat.timestamp.desc())

        if self.is_ajax_request():
            self.on_write_json({
                "draw": params['draw'],
                "recordsTotal": int(query.count()),
                "recordsFiltered": int(query.count()),
                "data": list(list(item.to_dict().values()) for item in query.limit(params['limit']).offset(offset).all())
            })
        else:
            self.on_write_page(template=self._template_file,
                               params={'title': 'Analytics Dashboard',
                                       'cols': VisitStat.__table__.columns.keys(),
                                       'items': query.limit(params['limit']).offset(offset).all(),
                                       'count': int(query.count()),
                                       'offset': offset,
                                       'static_url': self.static_url,
                                       **params})
