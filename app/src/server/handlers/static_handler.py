import tornado.web


class StaticHandler(tornado.web.StaticFileHandler):
    pass
    # def write_error(self, status_code, *args, **kwargs):
    #     if status_code in [404]:
    #         loader = tornado.template.Loader("./src/templates/")
    #         data = {
    #             'url': self.request.host,
    #             'urn': self.request.path,
    #             'uri': self.request.uri,
    #             'scheme': self.request.protocol,
    #         }
    #
    #         data.update(base.default_template_params)
    #         self.write(loader.load("404.html").generate(**data))
    #     else:
    #         super().write_error(status_code, *args, **kwargs)

