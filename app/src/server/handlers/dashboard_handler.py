from app.src import session
from app.src import Daily
from app.src.server.handlers.base import Base


class DashboardHandler(Base):
    _template_file = 'dashboard.html'

    def get(self):
        items = session().query(Daily).limit(1).all()

        self.on_write_page(template=self._template_file,
                           params={
                               'title': 'Dashboard',
                               'cols': Daily.__table__.columns.keys(),
                               'items': items
                           })
