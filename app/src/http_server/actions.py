from .handlers.analytics_handler import AnalyticsHandler
from .handlers.dashboard_handler import DashboardHandler
from .handlers.static_handler import StaticHandler

actions = [
    (r"/analytics/", AnalyticsHandler),
    (r"/analytics/dashboard/", DashboardHandler),

    (r"/analytics/static/(.*$)", StaticHandler, {"path": "./http_server/static"}),
    (r"/(.*$)", StaticHandler, {"path": "./http_server/static"}),
]
