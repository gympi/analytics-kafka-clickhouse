import inspect
import re
import time
import traceback
import uuid

import tornado.web


data = None
try:
    with open('./static/p.png', 'rb') as f:
        data = f.read()
except IOError as e:
    print("Error {}: ".format(inspect.currentframe().f_code.co_name), e)
    traceback.print_exc()


class PixelHandler(tornado.web.RequestHandler):
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

    def get(self):

        print('PixelHandler')
        print(len(self.request.cookies))
        print(self.get_cookie('analytic_uid'))

        # Uid user format
        # [int]        .  [uuid4]     .  [timestamp]
        # version uid  .  unique uid  .  timestamp create uid user

        # get or create cookie uid user
        uid_user = self.get_cookie('analytic_uid')

        regex_template = re.compile(r'\d\.[0-9a-f]{32}\.\d+')

        if re.match(regex_template, uid_user) is not None:
            pass
        else:
            uid_user = '1.' + str(uuid.uuid4().hex) + '.' + time.strftime("%s", time.gmtime())

        # update time cookie
        self.set_cookie('analytic_uid', uid_user, '.analytics.ru', time.time() + 86400)

        self.write(data)
        self.finish()
