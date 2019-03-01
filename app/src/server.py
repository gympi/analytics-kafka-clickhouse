#!/usr/bin/python3

# chmod +x ./server.py

import multiprocessing
import tornado.ioloop
import tornado.web
import tornado.httpserver

from http_server.actions import actions
from libs.system_environment import SystemEnvironment


def make_app():
    return tornado.web.Application(actions)


if __name__ == "__main__":
    # multiprocessing
    print('Create processes', multiprocessing.cpu_count() * 2)

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(SystemEnvironment().env['app']['port'])
    server.start(multiprocessing.cpu_count() * 2)
    tornado.ioloop.IOLoop.current().start()
