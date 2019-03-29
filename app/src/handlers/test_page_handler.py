from .base import Base


links = ('/', '/test_page_1/', '/test_page_2/', '/test_page_3/')


class TestMainPageHandler(Base):
    _template_file = 'test_page.html'

    def get(self):
        # self.set_cookie('analytic_uid', 'HelloServer', '.analytics.ru', time.time() + 86400)
        # self.write('Hello')
        # self.write('analytic_uid: ' + str(self.get_cookie('analytic_uid')))

        self.on_write_page(template=self._template_file,
                           params={'title': 'Test Main Page',
                                   'links': links})


class TestInnerPageHandler(Base):
    _template_file = 'test_page.html'

    def get(self, page):
        self.on_write_page(template=self._template_file,
                           params={'title': 'Test Inner Page',
                                   'links': links})
