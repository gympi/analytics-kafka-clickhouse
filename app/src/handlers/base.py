# import datetime
import json
import timeit
import tornado
import tornado.web

origin_urls = []


class Base(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._start_execute = timeit.default_timer()
        super(Base, self).__init__(application, request, **kwargs)

    def initialize(self):
        self._params = {}
        self._init_default_params()
        self._init_templates()
        self._init_helpers()

    def _init_templates(self):
        self._templates_path = "./templates/"
        self._template = "main.html"

    def _init_default_params(self):
        self.add_param({
            'url': self.request.host,
            'urn': self.request.path,
            'uri': self.request.uri,
            'query_params': self.request.query,
            'scheme': self.request.protocol,
        })

    def _init_helpers(self):
        pass

    def add_param(self, params: dict = None):
        if params is None:
            params = {}
        self._params.update(params)

    def set_default_headers(self):
        self.set_header('Server', 'Analytics')

        self.set_header('pragma', 'no-cache')
        self.set_header('Cache-Control', 'no-cache')
        # self.set_header('Expires', datetime.datetime.utcnow() + datetime.timedelta(minutes=1))

        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('X-Content-Type-Options', 'nosniff')
        self.set_header('Strict-Transport-Security', 'max-age=31536000')

        # self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Origin, Content-Type, X-Requested-With, Cache-Control, pragma')
        self.set_header('Access-Control-Allow-Credentials', 'true')

        self.clear_header('X-Frame-Options')

    def on_write_page(self, templates_path: str=None, template: str=None, params: dict=None):
        if not params is None:
            self.add_param(params)

        if not templates_path is None:
            self._templates_path = templates_path

        if not template is None:
            self._template = template

        loader = tornado.template.Loader(self._templates_path)
        self.write(loader.load(self._template).generate(**self._params))

        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.set_header("X-Time-app-build", '{:.5}'.format(str(timeit.default_timer() - self._start_execute)))

    def on_write_json(self, data=None):
        if data is None:
            data = {}

        self.write(json.dumps(data, default=str, separators=(',', ':')))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("X-Time-build", '{:.5}'.format(str(timeit.default_timer() - self._start_execute)))

    def throw_404_page_not_exist(self):
        self.set_status(404)
        self.on_write_page(template="404.html")

    def throw_head_404_page_not_exist(self):
        self.set_status(404)

    def is_ajax_request(self):
        return ("X-Requested-With" in self.request.headers and
                self.request.headers['X-Requested-With'] == "XMLHttpRequest") or (
                   'json' == self.get_argument('content_type', False))

    def options(self, *args, **kwargs):
        self.set_header("Allow", "OPTIONS, GET")
        self.finish()
