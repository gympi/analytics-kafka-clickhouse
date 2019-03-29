#!/usr/bin/env python3

# chmod +x ./server.py

import multiprocessing
import os

import tornado.ioloop
import tornado.web
import tornado.httpserver

from handlers.pixel_handler import PixelHandler
from handlers.test_page_handler import TestMainPageHandler, TestInnerPageHandler
from handlers.tick_handler import TickHandler
from libs.system_environment import SystemEnvironment


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "./static/"),
    "cookie_secret": "__GENERATE_RANDOM_VALUE_HERE__",
    # "login_url": "/login",
    "xsrf_cookies": True,
}

actions = [
    (r"/", TestMainPageHandler),
    (r"/test_page_(\d+)/", TestInnerPageHandler),
    (r"/set-cookie/", PixelHandler),

    (r"/tick/", TickHandler),
    (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))
]


def make_app():
    return tornado.web.Application(actions, **settings)


if __name__ == "__main__":
    # multiprocessing
    print('Create processes', multiprocessing.cpu_count() * 2)

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(SystemEnvironment().env['app']['port'])
    # server.start(multiprocessing.cpu_count() * 2)
    server.start(1)
    tornado.ioloop.IOLoop.current().start()
