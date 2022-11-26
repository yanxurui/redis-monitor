# monitor redis

## Introduction
This web app demonstrates a modern way of how to broadcast messages from the server to clients periodically via web socket which achieves similiar goal as server push. Comparred with the traditional long polling, web socket has better performance. For instance, if 100 clients are polling for the same resource, the server needs to repeat processing the same request 100 times which can reduced to just once using the model demonstrated here.

The application in this repo is to monitor the number of keys in a redis instance by executing the command INFO every second on the server side and sending the result to all clients. Based on this idea, you can do anything on the backend and broadcast the data to all connected clients in an efficient way.

## Usage
```bash
git clone git@github.com:yanxurui/redis-monitor.git
cd redis-monitor
pip install -r requirements.txt
python main.py
```
browser http://127.0.0.1:8000

config file is `conf.py`

## Development
Key techniques used in this demo

* Flask: the most popular web framework in the Python community
* gevent: enables requests to be processed in a concurrent manner via non-blocking IO
* web socket: achieve server push
