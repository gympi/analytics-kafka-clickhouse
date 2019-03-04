#!/usr/bin/env python3

# chmod +x ./server.py

import multiprocessing
import os

import tornado.ioloop
import tornado.web
import tornado.httpserver

from http_server.actions import actions
from libs.system_environment import SystemEnvironment


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "./http_server/static/"),
    "cookie_secret": "__GENERATE_RANDOM_VALUE_HERE__",
    # "login_url": "/login",
    "xsrf_cookies": True,
}


def make_app():
    return tornado.web.Application(actions, **settings)


if __name__ == "__main__":
    # multiprocessing
    print('Create processes', multiprocessing.cpu_count() * 2)

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(SystemEnvironment().env['app']['port'])
    server.start(multiprocessing.cpu_count() * 2)
    tornado.ioloop.IOLoop.current().start()
