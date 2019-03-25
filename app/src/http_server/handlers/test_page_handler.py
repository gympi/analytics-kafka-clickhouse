from http_server.handlers.base import Base


class TestMainPageHandler(Base):
    _template_file = 'test_page.html'

    def get(self):
        # self.set_cookie('analytic_uid', 'HelloServer', '.analytics.ru', time.time() + 86400)
        # self.write('Hello')
        # self.write('analytic_uid: ' + str(self.get_cookie('analytic_uid')))

        self.on_write_page(template=self._template_file,
                           params={'title': 'Test Main Page',
                                   'link': '/test_page/'})


class TestInnerPageHandler(Base):
    _template_file = 'test_page.html'

    def get(self):
        self.on_write_page(template=self._template_file,
                           params={'title': 'Test Inner Page',
                                   'link': '/'})
