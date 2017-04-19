import re
import json
import time
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import redis

import conf


class Handler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        # No 'Access-Control-Allow-Origin' header is present on the requested resource error
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == '/info':
            self._set_headers()
            data = {
                'time': time.strftime('%M:%S'),
                'keys': self._keys()
            }
            self.wfile.write(json.dumps(data))
        else:
            # serves static files from the current directory and below
            SimpleHTTPRequestHandler.do_GET(self)

    def _keys(self):
        r = redis.StrictRedis(host=conf.host, port=conf.port)
        info = r.info()
        return sum(v['keys'] for k,v in info.items() if re.match(r'db\d', k))


def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=Handler):
    PORT = 8000
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print('listening at %d...' % PORT)
    httpd.serve_forever()

if __name__ == '__main__':
    run()