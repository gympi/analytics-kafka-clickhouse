#!/usr/bin/python3

# chmod +x ./server.py

import sys
import multiprocessing

sys.path.append('../libs/')

from system_environment import SystemEnvironment
from app.src.server import actions

import tornado.ioloop
import tornado.web
import tornado.httpserver


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
