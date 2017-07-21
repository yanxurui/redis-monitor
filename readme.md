# monitor redis

## introduction
Monitor the number of keys in a redis instance by executing the command INFO every second.

## usage
```bash
git clone git@github.com:yanxurui/redis-monitor.git
cd redis-monitor
pip install -r requirements.txt
python main.py
```
browser http://127.0.0.1:8000

config file is `conf.py`

## dependeces
* Chart.js
* redis-py

## todo
- [ ] websocket
- [ ] used memory
- [ ] save snapshot
