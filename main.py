import re
import json
import time

import redis
import gevent
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from flask import Flask, send_from_directory

import conf

app = Flask(__name__)
# Catch-All URL
@app.route('/', defaults={'filename': ''})
@app.route('/<path:filename>')
def root(filename):
    # only serve static files for now
    if filename == '' or filename[-1] == '/':
        filename = filename + 'index.html'
    return send_from_directory('', filename)

class WSApp(WebSocketApplication):
    def on_open(self):
        print("Connected!")

    def on_close(self, reason):
        print("Connection closed!")

    def on_message(self, message):
        if message is None:
            pass # closed

server = WebSocketServer(('', conf.port), Resource([
        ('/info', WSApp),
        ('/', app)
    ]))

def keys():
    r = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port)
    info = r.info()
    return sum(v['keys'] for k,v in info.items() if re.match(r'db\d', k))

def beat():
    while True:
        gevent.sleep(conf.interval)
        if hasattr(server, 'clients') and server.clients:
            data = json.dumps({
                'time': time.strftime('%M:%S'),
                'keys': keys()
            })
            for client in server.clients.values():
                client.ws.send(data)

gevent.spawn(beat)

print('listening at %d...' % conf.port)
server.serve_forever()
