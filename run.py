#!/usr/bin/env python
import tornado.ioloop
from tornado.options import options
from proxy.app import create_app

import settings     # Required for options definitions


def main():
    app = create_app()
    app.listen(options.port)
    print("Puzzles Service Running on http://localhost:{port}".format(port=options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
