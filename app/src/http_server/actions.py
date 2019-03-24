from http_server.handlers.pixel_handler import PixelHandler
from http_server.handlers.test_page_handler import TestMainPageHandler, TestInnerPageHandler
from .handlers.tick_handler import TickHandler
from .handlers.static_handler import StaticHandler

actions = [
    (r"/", TestMainPageHandler),
    (r"/test_page/", TestInnerPageHandler),
    (r"/set-cookie/", PixelHandler),

    (r"/tick/", TickHandler),
    (r"/static/(.*$)", StaticHandler, {"path": "./http_server/static"}),
    (r"/(.*$)", StaticHandler, {"path": "./http_server/static"}),
]
