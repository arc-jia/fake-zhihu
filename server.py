import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=2333, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user_json = self.get_secure_cookie("chatdemo_user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):

    def get(self):
        self.render("index.html")


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
