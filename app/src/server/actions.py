from app.src.server.handlers import DashboardHandler
from .handlers.analytics_handler import AnalyticsHandler
from .handlers.static_handler import StaticHandler

actions = [
    (r"/analytics/dashboard/", DashboardHandler),
    (r"/analytics/", AnalyticsHandler),

    (r"/analytics/static/(.*$)", StaticHandler, {"path": "./static"}),
    (r"/(.*$)", StaticHandler, {"path": "./static"}),
]
