import os 
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = "127.0.0.1:5000" # 启动进程数量
workers = multiprocessing.cpu_count() * 2 +1
worker_class = "gevent"
worker_connections = 8000 
threads = 20
daemon = True
pidfile = "log/gunicorn.pid"
preload_app = True
x_forwarded_for_header = 'X_FORWARDED-FOR'

